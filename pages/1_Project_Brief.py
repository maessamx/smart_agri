import streamlit as st
from config import TEAM
from src.ui.component import initialize_page, hero, section_title, text_card, bullet_card, accent_card

st.set_page_config(page_title='Project Brief | Smart Agri Egypt', page_icon='📘', layout='wide')
initialize_page()
hero('Project Presentation', 'Smart Agri Egypt is a data-driven agricultural platform developed as a Summer Training project for the Faculty of Engineering, Capital University.')

st.markdown("<span class='badge'>COMPUTER AND SYSTEMS ENGINEERING DEPARTMENT</span>", unsafe_allow_html=True)
section_title('Project Vision')
text_card('Agricultural Decision Support', 'Smart Agri Egypt transforms governorate-level agricultural records into an interactive decision-support platform. It enables users to compare products, identify major cultivation locations, visualize crop distribution, and explore agricultural indicators in a single interface.')

first, second, third = st.columns(3)
with first:
    accent_card('Challenge', 'Agricultural information is often fragmented across reports and difficult to compare quickly across products and locations.', 'gold')
with second:
    accent_card('Solution', 'An interactive web dashboard that organizes crop records into clear rankings, maps, and visual analytics.', 'blue')
with third:
    accent_card('Impact', 'A scalable foundation for future irrigation monitoring, fertilizer advice, and production forecasting.', 'purple')

section_title('Project Objectives')
left, right = st.columns(2)
with left:
    bullet_card('Analytics Objectives', ['Compare common crops across Egypt’s governorates.', 'Identify leading cultivation locations for each product.', 'Visualize area, production, yield, and category composition.'])
with right:
    bullet_card('Development Objectives', ['Create a reusable multi-page Streamlit architecture.', 'Train an irrigation-decision model from the provided dataset.', 'Prepare dedicated modules for fertilizer and production planning.'])

section_title('System Architecture')
architecture = st.columns(3)
with architecture[0]: accent_card('1. Data Layer', 'Agricultural crop records, irrigation training data, and dynamic governorate boundary geometry.', 'gold')
with architecture[1]: accent_card('2. Analytics Layer', 'Data preparation, product aggregation, crop ranking, model inference, and visualization logic.', 'blue')
with architecture[2]: accent_card('3. Application Layer', 'Interactive Streamlit pages, Folium maps, Matplotlib charts, and decision-support interfaces.', 'purple')

section_title('Technology Stack')
bullet_card('Core Technologies', ['Python and Streamlit for the web application.', 'Pandas for cleaning and aggregation.', 'Folium and GeoJSON for interactive maps.', 'Matplotlib and Plotly for charts.', 'Scikit-learn Random Forest for irrigation classification.'])

section_title('Summer Training Team')
bullet_card('Contributors', TEAM)
