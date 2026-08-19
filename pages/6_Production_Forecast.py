import streamlit as st
from src.ui.component import initialize_page, coming_soon

st.set_page_config(page_title='Production Forecast | Smart Agri Egypt', page_icon='📈', layout='wide')
initialize_page()
coming_soon('Production Forecast', 'This page will estimate expected production using farm area, crop type, governorate, historical yield, soil measurements, weather conditions, and seasonal indicators.')
