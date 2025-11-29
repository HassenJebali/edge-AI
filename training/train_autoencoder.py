import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from utils.preprocess import compute_scaler
FEATURES = ['temp','hum','water','light','fan_pwm']
def load_data(path):
df = pd.read_csv(path)
return df
if __name__ == '__main__':
df = load_data('data/simulated/autoenc_train.csv')
mean,std = compute_scaler(df, FEATURES)
X = (df[FEATURES].values - mean)/std
Xtr, Xte = train_test_split(X, test_size=0.2, random_state=42)
input_dim = Xtr.shape[1]
inp = tf.keras.layers.Input(shape=(input_dim,))
enc = tf.keras.layers.Dense(16, activation='relu')(inp)
enc = tf.keras.layers.Dense(8, activation='relu')(enc)
dec = tf.keras.layers.Dense(16, activation='relu')(enc)
out = tf.keras.layers.Dense(input_dim, activation='linear')(dec)
model = tf.keras.Model(inputs=inp, outputs=out)
model.compile(optimizer='adam', loss='mse')
model.fit(Xtr, Xtr, validation_data=(Xte,Xte), epochs=50, batch_size=64)
model.save('models/anomaly/saved_model')
print('saved')
