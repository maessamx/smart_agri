import streamlit as st
from src.ui.component import initialize_page, coming_soon

st.set_page_config(page_title='Irrigation & Fertilizer | Smart Agri Egypt', page_icon='💧', layout='wide')
initialize_page()
coming_soon('Irrigation & Fertilizer', 'This module will connect soil moisture, NPK, pH, weather data, and farm-specific rules to support irrigation and fertilizer decisions.')
