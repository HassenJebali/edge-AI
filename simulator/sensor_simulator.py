"""
Simple sensor simulator that publishes JSON telemetry to MQTT.
Publishes to topic: cold/temperature
"""
import time
import json
import argparse
from datetime import datetime
import numpy as np
import paho.mqtt.client as mqtt

DEFAULT_BROKER = 'localhost'
DEFAULT_PORT = 1883
def gen_baseline_step(state, dt_s=1.0):
# A simple physical-like step update
# state is dict: temp, hum, water, light, fan_pwm
# fan reduces temp slightly; door (light) increases temp faster
# add Gaussian noise
temp = state['temp']
hum = state['hum']
water = state['water']
light = state['light']
fan = state['fan_pwm']
# fan effect: scale with pwm (0-255)
fan_effect = (fan / 255.0) * 0.05
# ambient drift toward 6.0C
ambient = 6.0
temp += (ambient - temp) * 0.001 # slow thermal coupling
temp -= fan_effect * 0.02
# if door open (light==1) add heat
if light >= 0.5:
temp += 0.02
# humidity interplay
hum += (50.0 - hum) * 0.0005
hum += np.random.normal(0, 0.05)
# water level can slowly increase if condensation
water += -0.0001 + np.random.normal(0, 0.001)
if water < 0: water = 0.0
# noise on temp
temp += np.random.normal(0, 0.02)
state['temp'] = float(np.round(temp, 3))
state['hum'] = float(np.round(hum, 3))
state['water'] = float(np.round(water, 4))
return state

def publish_loop(broker='localhost', port=1883, rate_hz=1.0, scenario=None):
client = mqtt.Client()
client.connect(broker, port)
state = {'temp':6.0, 'hum':70.0, 'water':0.1, 'light':0.0, 'fan_pwm':80}
t = 0
try:
while True:
# modify state for scenarios
if scenario == 'heat_ramp' and t>10:
state['temp'] += 0.05
if scenario == 'door_open' and 30 < t < 90:
state['light'] = 1.0
if scenario == 'water_leak' and t>60:
state['water'] += 0.01
if scenario == 'fan_block' and t>20:
state['fan_pwm'] = 0
state = gen_baseline_step(state)
payload = {
'ts': datetime.utcnow().isoformat() + 'Z',
'temp': state['temp'],
'hum': state['hum'],
'water': state['water'],
'light': state['light'],
'fan_pwm': state['fan_pwm']
}
client.publish('cold/temperature', json.dumps(payload), qos=0)
t += 1
time.sleep(1.0/ rate_hz)
except KeyboardInterrupt:
print('stopped')
if __name__ == '__main__':
parser = argparse.ArgumentParser()
parser.add_argument('--broker', default=DEFAULT_BROKER)
parser.add_argument('--port', default=DEFAULT_PORT, type=int)
parser.add_argument('--rate', default=1.0, type=float)
parser.add_argument('--scenario', default=None,
choices=['heat_ramp','door_open','water_leak','fan_block',None])
args = parser.parse_args()
publish_loop(broker=args.broker, port=args.port, rate_hz=args.rate,
scenario=args.scenario)
