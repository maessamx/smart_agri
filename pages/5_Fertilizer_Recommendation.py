import streamlit as st
from src.ui.component import initialize_page, coming_soon

st.set_page_config(page_title='Fertilizer Recommendation | Smart Agri Egypt', page_icon='🧪', layout='wide')
initialize_page()
coming_soon('Fertilizer Recommendation', 'This page will recommend fertilizer type and quantity using crop type, NPK readings, soil pH, field area, crop growth stage, and soil-test results.')
