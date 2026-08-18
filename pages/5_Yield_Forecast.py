import streamlit as st
from src.ui.component import initialize_page, coming_soon

st.set_page_config(page_title='Yield Forecast | Smart Agri Egypt', page_icon='📈', layout='wide')
initialize_page()
coming_soon('Yield Forecast', 'This module will estimate expected crop production using cultivated area, crop type, location, historical yield, soil conditions, and seasonal factors.')
