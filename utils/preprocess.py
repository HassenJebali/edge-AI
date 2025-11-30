"""
Feature engineering and scaler utilities.
Compute mean/std on training dataset and save scaler as numpy file.
"""
import numpy as np
import pandas as pd
import joblib

SCALER_PATH = 'models/scaler.npz'

def compute_scaler(df,feature_cols=['temp','hum','water','light','fan_pwm']):
    arr = df[feature_cols].values.astype(np.float32)
    mean = arr.mean(axis=0)
    std = arr.std(axis=0) + 1e-6
    np.savez(SCALER_PATH, mean=mean, std=std)
    return mean, std

def load_scaler():
    d = np.load(SCALER_PATH)
    return d['mean'], d['std']
