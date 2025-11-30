import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from utils.preprocess import compute_scaler

FEATURES = ['temp','hum','water','light','fan_pwm']
LABELS = ['fan_pwm_opt','pump_dur']

def load_data(path):
    df = pd.read_csv(path)
    return df

if __name__ == '__main__':
    df = load_data('data/simulated/opt_train.csv')
    mean,std = compute_scaler(df, FEATURES)
    X = (df[FEATURES].values - mean)/std
    y = df[LABELS].values
    Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=0.2, random_state=42)
    model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(len(FEATURES),)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(2, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(Xtr, ytr, validation_data=(Xte,yte), epochs=40, batch_size=64)
    model.save('models/optimization/saved_model')
    print('saved')
