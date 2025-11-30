"""
Simulated STM32: subscribes to sensor topic, runs TFLite inference for three
models
- prediction (binary)
- anomaly (autoencoder: compute recon error)
- optimization (regression)
Publishes anomalies and optimization to MQTT.
"""
import json
import time
import numpy as np
import paho.mqtt.client as mqtt
import argparse

from datetime import datetime
# tflite-runtime interpreter import
try:
    import tensorflow.lite as tflite
except Exception:
    # fallback to tensorflow lite if runtime not installed
    import tensorflow as tf
    tflite = None

BROKER='localhost'

# Paths to .tflite; replace with actual paths after conversion
PRED_TFLITE = 'tflite/pred_model.tflite'
ANOM_TFLITE = 'tflite/autoenc_model.tflite'
OPT_TFLITE = 'tflite/opt_model.tflite'

# simple normalization config (these numbers would be computed in preprocess)
MEAN = np.array([6.0,70.0,0.1,0.0,80.0], dtype=np.float32)
STD = np.array([2.0,5.0,0.2,1.0,60.0], dtype=np.float32)

class ModelWrapper:
    def __init__(self, path):
        if tflite is not None and hasattr(tflite, 'Interpreter'):
            self.interp = tflite.Interpreter(path)
        else:
            self.interp = tf.lite.Interpreter(path)
            self.interp.allocate_tensors()
            self.in_idx = self.interp.get_input_details()[0]['index']
            self.out_idx = self.interp.get_output_details()[0]['index']
    def infer(self, x:np.ndarray):
        # x must be shaped correctly
        self.interp.set_tensor(self.in_idx, x)
        self.interp.invoke()
        out = self.interp.get_tensor(self.out_idx)
        return out

# buffer for recent samples
data_buffer = []
BUFFER_SIZE = 100

# instantiate later
pred_model = None
anom_model = None
opt_model = None
mqtt_client = None


def normalize(sample):
    x = np.array([sample['temp'], sample['hum'], sample['water'],
sample['light'], sample['fan_pwm']], dtype=np.float32)
    return (x - MEAN)/STD

def on_connect(client, userdata, flags, rc):
    print('connected rc=', rc)
    client.subscribe('cold/temperature', qos=0)

def on_message(client, userdata, msg):
    global data_buffer
    payload = json.loads(msg.payload.decode())
    # append to buffer
    data_buffer.append(payload)
    if len(data_buffer) > BUFFER_SIZE:
        data_buffer.pop(0)


# build features - here we use last sample only for simplicity
x_raw = normalize(payload)
x = x_raw.reshape(1, -1).astype(np.float32)

# prediction model
try:
    pred_out = pred_model.infer(x)
    pred_score = float(pred_out[0][0])
except Exception as e:
    pred_score = 0.0

# anomaly: compute recon error (autoencoder)
try:
    recon = anom_model.infer(x)
    recon = recon.reshape(-1)
    err = float(np.mean((recon - x_raw)**2))
except Exception as e:
    err = 0.0
# optimization
try:
    opt_out = opt_model.infer(x)
    fan_pwm = float(opt_out[0][0])
    pump_dur = float(opt_out[0][1])
except Exception as e:
    fan_pwm = payload.get('fan_pwm', 0)
    pump_dur = 0.0

# simple thresholds
if pred_score > 0.5:
    client.publish('cold/anomalies',
    json.dumps({'ts':datetime.utcnow().isoformat()
    +'Z','type':'predicted_threshold','score':pred_score}), qos=1)

# anomaly threshold (example)
if err > 0.1:
    client.publish('cold/anomalies',
    json.dumps({'ts':datetime.utcnow().isoformat()
    +'Z','type':'reconstruction','error':err}), qos=1)

# publish optimization
    client.publish('cold/optimization',
json.dumps({'ts':datetime.utcnow().isoformat()
+'Z','fan_pwm':fan_pwm,'pump_duration':pump_dur}), qos=0)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--broker', default=BROKER)
    parser.add_argument('--port', default=1883, type=int)
    args = parser.parse_args()
    # load models
    print('Loading models...')
    pred_model = ModelWrapper(PRED_TFLITE)
    anom_model = ModelWrapper(ANOM_TFLITE)
    opt_model = ModelWrapper(OPT_TFLITE)
    print('Models loaded')
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(args.broker, args.port)
    mqtt_client.loop_forever()
