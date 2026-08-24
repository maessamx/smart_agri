import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from .preprocessing import FEATURES, TARGET, build_preprocessor, clean_irrigation_data

MODEL_PARAMETERS = {
    'n_estimators': 300,
    'random_state': 42,
    'n_jobs': -1
}

@st.cache_resource
def train_model():
    data = clean_irrigation_data()
    features = data[FEATURES]
    target = data[TARGET]
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.20,
        random_state=42,
        stratify=target
    )
    evaluation_model = Pipeline([
        ('preprocessor', build_preprocessor()),
        ('classifier', RandomForestClassifier(**MODEL_PARAMETERS))
    ])
    evaluation_model.fit(x_train, y_train)
    accuracy = accuracy_score(y_test, evaluation_model.predict(x_test))
    deployment_model = Pipeline([
        ('preprocessor', build_preprocessor()),
        ('classifier', RandomForestClassifier(**MODEL_PARAMETERS))
    ])
    deployment_model.fit(features, target)
    metrics = {
        'accuracy': float(accuracy),
        'training_records': len(x_train),
        'testing_records': len(x_test),
        'classes': sorted(target.unique().tolist())
    }
    return deployment_model, data, metrics

def predict(input_data):
    model, _, _ = train_model()
    predicted_class = int(model.predict(input_data)[0])
    confidence = float(model.predict_proba(input_data)[0].max())
    return predicted_class, confidence
