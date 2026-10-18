from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parents[3] / 'data' / 'fertilizer' / 'fertilizer_prediction.csv'
SAMPLE_FRACTION = 0.4


@st.cache_data
def load_fertilizer_data():
    data = pd.read_csv(DATA_PATH)
    return data.rename(columns={
        'Temparature': 'temperature',
        'Humidity': 'humidity',
        'Moisture': 'moisture',
        'Soil Type': 'soil_type',
        'Crop Type': 'crop_type',
        'Nitrogen': 'nitrogen',
        'Potassium': 'potassium',
        'Phosphorous': 'phosphorous',
        'Fertilizer Name': 'fertilizer_name'
    })


@st.cache_data
def load_training_sample(sample_fraction=SAMPLE_FRACTION, random_state=42):
    data = load_fertilizer_data()
    groups = list(data.groupby(['crop_type', 'fertilizer_name'], sort=True))
    sampled_parts = [
        group.sample(
            n=max(1, round(len(group) * sample_fraction)),
            random_state=random_state
        )
        for _, group in groups
    ]
    sampled = pd.concat(sampled_parts)
    return sampled.sample(frac=1, random_state=random_state)
