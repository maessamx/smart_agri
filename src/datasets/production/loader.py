from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parents[3] / 'data' / 'production' / 'production_prediction.csv'


@st.cache_data
def load_production_data():
    return pd.read_csv(DATA_PATH)


@st.cache_data
def load_training_sample():
    return load_production_data()
