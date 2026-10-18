from time import perf_counter

import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.datasets.fertilizer.loader import (
    load_fertilizer_data,
    load_training_sample
)


FEATURES = [
    'temperature', 'moisture', 'soil_type', 'crop_type',
    'nitrogen', 'potassium', 'phosphorous'
]


@st.cache_resource
def train_fertilizer_model():
    started = perf_counter()
    original = load_fertilizer_data()
    data = load_training_sample()
    x = data[FEATURES]
    y = data['fertilizer_name']

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=data[['crop_type', 'fertilizer_name']].astype(str).agg('|'.join, axis=1)
    )

    preprocessing = ColumnTransformer([
        ('categories', OneHotEncoder(handle_unknown='ignore'), ['soil_type', 'crop_type'])
    ], remainder='passthrough')

    model = Pipeline([
        ('preprocessing', preprocessing),
        ('classifier', RandomForestClassifier(
            n_estimators=80,
            max_depth=18,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ))
    ])

    model.fit(x_train, y_train)
    train_prediction = model.predict(x_train)
    test_prediction = model.predict(x_test)
    labels = sorted(y.unique())
    metrics = {
        'original_rows': len(original),
        'filtered_rows': len(original),
        'final_rows': len(data),
        'train_rows': len(x_train),
        'test_rows': len(x_test),
        'crops_kept': sorted(data['crop_type'].unique()),
        'crops_removed': sorted(set(original['crop_type']) - set(data['crop_type'])),
        'class_counts': data['fertilizer_name'].value_counts().sort_index().to_dict(),
        'train_accuracy': accuracy_score(y_train, train_prediction),
        'test_accuracy': accuracy_score(y_test, test_prediction),
        'labels': labels,
        'confusion_matrix': confusion_matrix(y_test, test_prediction, labels=labels).tolist(),
        'classification_report': classification_report(
            y_test,
            test_prediction,
            labels=labels,
            output_dict=True,
            zero_division=0
        ),
        'training_seconds': perf_counter() - started
    }
    return model, metrics


def predict_fertilizer(values):
    model, metrics = train_fertilizer_model()
    sample = pd.DataFrame([values], columns=FEATURES)
    prediction = model.predict(sample)[0]
    confidence = model.predict_proba(sample).max()
    return prediction, confidence, metrics['test_accuracy']
