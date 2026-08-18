import streamlit as st
from config import TEAM
from src.ui.component import initialize_page, hero, section_title, text_card, bullet_card

st.set_page_config(page_title='Project Brief | Smart Agri Egypt', page_icon='📘', layout='wide')
initialize_page()
hero('Project Presentation', 'A structured overview of the Smart Agri Egypt platform for academic presentation and evaluation.')

section_title('Problem Statement')
text_card('Agricultural Decision Support', 'Agricultural data is often fragmented and difficult to use in daily decision-making. Smart Agri Egypt organizes governorate-level crop records into an interactive platform that supports crop comparison, spatial analysis, and future smart-farm expansion.')

left, right = st.columns(2)
with left:
    bullet_card('Objectives', ['Compare common crops across Egypt’s governorates.', 'Identify leading cultivation locations for each product.', 'Visualize agricultural patterns through maps and charts.', 'Provide a scalable foundation for smart irrigation and crop forecasting.'])
with right:
    bullet_card('Technology Stack', ['Streamlit for the interactive interface.', 'Pandas for data preparation and aggregation.', 'Folium for interactive geographic visualization.', 'Matplotlib and Plotly for analytical charts.'])

section_title('System Architecture')
text_card('Workflow', 'Data layer — agricultural crop records. Analytics layer — cleaning, filtering, aggregation, and ranking. Presentation layer — Streamlit pages, maps, and charts.')
section_title('Future Scope')
text_card('Extensibility', 'The project structure supports future integration with soil sensors, real-time weather data, crop recommendation models, farm notifications, irrigation automation, and production forecasting models.')
section_title('Contributors')
bullet_card('Summer Training Team', TEAM)
