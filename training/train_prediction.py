"""
Train a dense binary classifier to predict threshold crossing in the next N seconds.
"""
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from utils.preprocess import compute_scaler
FEATURES = ['temp','hum','water','light','fan_pwm']
# load CSV training data prepared in data/simulated/
# Each sample must include future label 'label_5min'
def load_data(path):
df = pd.read_csv(path)
return df
if __name__ == '__main__':
df = load_data('data/simulated/pred_train.csv')
# compute scaler
mean,std = compute_scaler(df, FEATURES)
X = (df[FEATURES].values - mean)/std
y = df['label_5min'].values
Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=0.2, random_state=42)
model = tf.keras.Sequential([
tf.keras.layers.Input(shape=(len(FEATURES),)),
tf.keras.layers.Dense(64, activation='relu'),
tf.keras.layers.Dense(32, activation='relu'),
tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy',
metrics=['accuracy'])
model.fit(Xtr, ytr, validation_data=(Xte,yte), epochs=30, batch_size=64)
model.save('models/prediction/saved_model')
print('saved')
