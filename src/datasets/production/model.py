from time import perf_counter

import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.datasets.production.loader import (
    load_production_data,
    load_training_sample
)


FEATURES = ['crop_type', 'soil_type', 'season', 'ground_area_feddan']


@st.cache_resource
def train_production_model():
    started = perf_counter()
    original = load_production_data()
    data = load_training_sample()
    x = data[FEATURES]
    y = data['yield_ton_per_feddan']

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    preprocessing = ColumnTransformer([
        ('categories', OneHotEncoder(handle_unknown='ignore'),
         ['crop_type', 'soil_type', 'season'])
    ], remainder='passthrough')

    model = Pipeline([
        ('preprocessing', preprocessing),
        ('regressor', RandomForestRegressor(
            n_estimators=150,
            max_depth=12,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        ))
    ])

    model.fit(x_train, y_train)
    train_prediction = model.predict(x_train)
    test_prediction = model.predict(x_test)

    metrics = {
        'original_rows': len(original),
        'final_rows': len(data),
        'train_rows': len(x_train),
        'test_rows': len(x_test),
        'crops_covered': sorted(data['crop_type'].unique()),
        'train_r2': r2_score(y_train, train_prediction),
        'test_r2': r2_score(y_test, test_prediction),
        'test_mae': mean_absolute_error(y_test, test_prediction),
        'training_seconds': perf_counter() - started
    }
    return model, metrics


def predict_production(values, ground_area_feddan=1.0):
    model, metrics = train_production_model()
    sample = pd.DataFrame([values], columns=FEATURES)
    yield_per_feddan = model.predict(sample)[0]
    total_production = yield_per_feddan * ground_area_feddan
    return yield_per_feddan, total_production, metrics['test_r2']
