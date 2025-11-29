"""
Simple Streamlit app to subscribe to MQTT via a local relay that writes CSV,
or reading CSV.
This example reads a CSV file (data/stream.csv) that simulator can append to.
"""
import streamlit as st
import pandas as pd
import time
st.title('ColdStorage Dashboard (simple)')
DATA_PATH = 'data/stream.csv'
st.sidebar.header('Controls')
refresh = st.sidebar.button('Refresh Now')
@st.cache(ttl=5)
def load_data():
try:
df = pd.read_csv(DATA_PATH)
except Exception:
df = pd.DataFrame()
return df
if refresh:
df = load_data()
else:
df = load_data()
if df.empty:
st.write('No data yet. Run the simulators and append to data/stream.csv')
else:
st.line_chart(df[['temp','hum']].tail(500))
st.table(df.tail(10))
