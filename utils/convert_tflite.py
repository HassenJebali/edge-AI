"""
Convert Keras saved models to .tflite; simple quantization example.
"""
import tensorflow as tf
import numpy as np

def convert(saved_model_dir, out_path, quantize=False, representative_data=None):
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    if quantize:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        if representative_data is not None:
            def gen():
                for x in representative_data:
                    yield [x]
                converter.representative_dataset = gen
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.int8
        converter.inference_output_type = tf.int8
    tflite_model = converter.convert()
    with open(out_path, 'wb') as f:
        f.write(tflite_model)
    print('wrote', out_path)
if __name__ == '__main__':
# example usage: provide your saved_model directories
    pass
