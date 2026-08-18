import streamlit as st
from pathlib import Path
from config import PROJECT_NAME, PROJECT_SUBTITLE, TEAM
from src.data_service import load_records
from src.ui.component import initialize_page, hero, section_title, info_card, bullet_card

st.set_page_config(page_title=PROJECT_NAME, page_icon='🌿', layout='wide')
initialize_page()
ROOT = Path(__file__).parent
records = load_records()

st.image(str(ROOT / 'assets' / 'smart_agri_logo.svg'), width=310)
hero('Smart Agri Egypt', PROJECT_SUBTITLE)

col1, col2, col3 = st.columns(3)
features = [
    ('🌱', 'Crop Intelligence', 'Explore crop performance across Egypt and identify the leading governorates for each product.'),
    ('🗺️', 'Geographic Analytics', 'Use map-based visualizations and comparative charts to understand crop distribution.'),
    ('📊', 'Data Analytics', 'Analyze area, production, yield, and category composition across all governorates.'),
]
for col, (icon, title, text) in zip([col1, col2, col3], features):
    with col:
        info_card(title, text, icon)

section_title('Project Snapshot')
a, b, c, d = st.columns(4)
a.metric('Governorates', records['governorate'].nunique())
b.metric('Selected products', records['product'].nunique())
c.metric('Product categories', records['product_category'].nunique())
d.metric('Data records', f"{len(records):,}")

section_title('Contributors')
bullet_card('Summer Training Team', TEAM)
st.caption('Use Quick Navigation at the top of the page to open each project module.')
