import streamlit as st

from src.datasets.production.loader import load_training_sample
from src.datasets.production.model import predict_production, train_production_model
from src.ui.component import initialize_page, hero, section_title

st.set_page_config(page_title='Production Forecast | Smart Agri Egypt', page_icon='📈', layout='wide')
initialize_page()

data = load_training_sample()

hero(
    'Production Forecast',
    'Enter the crop type, soil type, season, and ground area to estimate expected production, '
    'based on real Egyptian governorate-level agriculture records.'
)

model, metrics = train_production_model()

first, second = st.columns(2)
with first:
    crop = st.selectbox('Crop Type', sorted(data['crop_type'].unique()))
    soil = st.selectbox('Soil Type', sorted(data['soil_type'].unique()))
with second:
    season = st.selectbox('Season', sorted(data['season'].unique()))
    ground_area = st.slider(
        'Ground Area (feddan)',
        float(data['ground_area_feddan'].min()),
        float(data['ground_area_feddan'].max()),
        float(data['ground_area_feddan'].median())
    )

run_prediction = st.button('Predict Production')

section_title('Model Status')
a, b, c = st.columns(3)
a.metric('Training Dataset Rows', f'{metrics["final_rows"]:,}')
b.metric('Crops Covered', len(metrics['crops_covered']))
c.metric('Model Fit (R²)', f'{metrics["test_r2"]:.2f}')

if run_prediction:
    values = {
        'crop_type': crop,
        'soil_type': soil,
        'season': season,
        'ground_area_feddan': ground_area
    }
    yield_per_feddan, total_production, r2 = predict_production(values, ground_area_feddan=ground_area)

    section_title('Prediction Result')
    result, total, fit = st.columns(3)
    result.metric('Estimated Yield', f'{yield_per_feddan:,.2f} ton/feddan')
    total.metric(f'Total Production ({ground_area:g} feddan)', f'{total_production:,.1f} ton')
    fit.metric('Model Fit (R²)', f'{r2:.2f}')

    st.success(
        f'For a {ground_area:g} feddan {crop} farm on {soil} soil during the {season} season, '
        f'the model estimates about {total_production:,.1f} tons of total production.'
    )
