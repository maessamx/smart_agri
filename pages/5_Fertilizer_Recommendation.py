import streamlit as st
from src.datasets.fertilizer.loader import load_training_sample
from src.datasets.fertilizer.model import predict_fertilizer, train_fertilizer_model
from src.ui.component import initialize_page, hero, section_title

st.set_page_config(page_title='Fertilizer Recommendation | Smart Agri Egypt', page_icon='🧪', layout='wide')
initialize_page()
data = load_training_sample()

hero('Fertilizer Prediction', 'Enter the field conditions and nutrient readings used by the supplied dataset to predict a fertilizer name.')

model, metrics = train_fertilizer_model()

first, second = st.columns(2)
with first:
    crop = st.selectbox('Crop Type', sorted(data['crop_type'].unique()))
    soil = st.selectbox('Soil Type', sorted(data['soil_type'].unique()))
    temperature = st.slider('Temperature (°C)', int(data['temperature'].min()), int(data['temperature'].max()), 30)
    moisture = st.slider('Soil Moisture', int(data['moisture'].min()), int(data['moisture'].max()), 45)

with second:
    nitrogen = st.slider('Nitrogen Level', int(data['nitrogen'].min()), int(data['nitrogen'].max()), 23)
    phosphorous = st.slider('Phosphorous Level', int(data['phosphorous'].min()), int(data['phosphorous'].max()), 21)
    potassium = st.slider('Potassium Level', int(data['potassium'].min()), int(data['potassium'].max()), 9)

run_prediction = st.button('Predict Fertilizer')

section_title('Model Status')
a, b = st.columns(2)
a.metric('Training Dataset Rows', f'{metrics["final_rows"]:,}')
b.metric('Fertilizer Classes', data['fertilizer_name'].nunique())

if run_prediction:
    values = {
        'temperature': temperature,
        'moisture': moisture,
        'soil_type': soil,
        'crop_type': crop,
        'nitrogen': nitrogen,
        'potassium': potassium,
        'phosphorous': phosphorous
    }
    fertilizer, confidence, accuracy = predict_fertilizer(values)
    section_title('Prediction Result')
    result, certainty = st.columns(2)
    result.metric('Suggested Fertilizer', fertilizer)
    certainty.metric('Prediction Confidence', f'{confidence:.1%}')
    st.success(f'The model selected {fertilizer} for the entered conditions.')
