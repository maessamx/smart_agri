from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]

PAGES = [
    ('pages/1_Project_Brief.py', 'Project Brief', '📘'),
    ('pages/2_Crop_Intelligence.py', 'Crop Intelligence', '🌱'),
    ('pages/4_Irrigation_Control.py', 'Irrigation Control', '💧'),
    ('pages/5_Fertilizer_Recommendation.py', 'Fertilizer', '🧪'),
    ('pages/6_Production_Forecast.py', 'Production Forecast', '📈'),
]
def inject_ui():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');
    html,body,[class*="css"]{font-family:"DM Sans",sans-serif}.stApp{background:#F5F8F2;color:#173B2B}header,footer,#MainMenu{visibility:hidden}.block-container{max-width:1470px;padding-top:1.15rem;padding-bottom:2.5rem}
    .hero{background:radial-gradient(circle at 85% 15%,rgba(180,217,110,.32),transparent 23%),linear-gradient(120deg,#0E3F2E,#1D6747 56%,#679A4D);border-radius:25px;padding:2.3rem 2.5rem;color:white;box-shadow:0 12px 32px rgba(16,63,46,.2);margin-bottom:1.2rem}.eyebrow{font-size:.78rem;letter-spacing:2px;font-weight:700;opacity:.76}.hero h1{font-family:"Playfair Display",serif;font-size:2.5rem;margin:.35rem 0}.hero p{max-width:820px;font-size:1.03rem;line-height:1.7;margin:0;opacity:.92}
    .section-title{font-family:"Playfair Display",serif;color:#174E37;font-size:1.55rem;margin:1.4rem 0 .45rem}.card{height:100%;box-sizing:border-box;background:#fff;border:1px solid #DDEBDD;border-top:4px solid #67A659;border-radius:18px;padding:1.15rem 1.25rem;box-shadow:0 7px 20px rgba(22,62,38,.07)}.card.blue{border-top-color:#3C82B5}.card.gold{border-top-color:#E5A93F}.card.purple{border-top-color:#8769AF}.card h3{margin:.1rem 0 .5rem;color:#17543A}.muted{color:#65766C;line-height:1.65;font-size:.92rem}.badge{display:inline-block;background:#E7F1DD;color:#26603E;padding:.25rem .6rem;border-radius:999px;font-size:.76rem;font-weight:700}.stButton>button{background:#216C49;color:white;border:0;border-radius:10px;font-weight:700;padding:.56rem .9rem}.stButton>button:hover{background:#144C35;color:white}.stMetric{background:white;border:1px solid #E1E9DE;border-radius:14px;padding:.55rem}.top-navigation{font-size:.72rem;letter-spacing:1.5px;color:#5A7767;font-weight:700;margin:.1rem 0 .35rem}.callout{background:#EBF5E4;border-left:4px solid #73A955;border-radius:8px;padding:.8rem 1rem;color:#24523A}
    </style>""", unsafe_allow_html=True)


def initialize_page():
    inject_ui()
    render_top_navigation()


def render_top_navigation():
    st.markdown("<div class='top-navigation'><span>QUICK NAVIGATION</span></div>", unsafe_allow_html=True)
    row_one = st.columns(3)
    row_one[0].page_link('app.py', label='Home', icon='🏠')
    row_one[1].page_link('pages/1_Project_Brief.py', label='Brief', icon='📘')
    row_one[2].page_link('pages/2_Crop_Intelligence.py', label='Crop Intelligence', icon='🌱')
    row_two = st.columns(3)
    row_two[0].page_link('pages/4_Irrigation_Control.py', label='Irrigation Control', icon='💧')
    row_two[1].page_link('pages/5_Fertilizer_Recommendation.py', label='Fertilizer', icon='🧪')
    row_two[2].page_link('pages/6_Production_Forecast.py', label='Production Forecast', icon='📈')
    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

def hero(title, text, eyebrow='SMART AGRI EGYPT · AGRICULTURAL INTELLIGENCE'):
    st.markdown(f"<section class='hero'><div class='eyebrow'>{eyebrow}</div><h1>{title}</h1><p>{text}</p></section>", unsafe_allow_html=True)

def section_title(title):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)

def info_card(title, text, icon=None):
    icon_html = f"<div style='font-size:1.7rem'>{icon}</div>" if icon else ''
    st.markdown(f"<div class='card'>{icon_html}<h3>{title}</h3><p class='muted'>{text}</p></div>", unsafe_allow_html=True)

def coming_soon(title, text):
    hero(title, text)
    st.markdown("<div class='card'><span class='badge'>NEXT DEVELOPMENT PHASE</span><h3>Coming Soon</h3><p class='muted'>This module has been reserved in the platform structure and will be connected to its data and decision logic in a future release.</p></div>", unsafe_allow_html=True)

def menu_card(page_path, title, text, icon):
    with st.container(border=True):
        st.markdown(f"### {icon} {title}")
        st.caption(text)
        st.page_link(page_path, label=f'Open {title}', icon='📂')

def text_card(title, text):
    st.markdown(f"<div class='card'><h3>{title}</h3><p class='muted'>{text}</p></div>", unsafe_allow_html=True)

def bullet_card(title, items):
    content = ''.join(f'<li>{item}</li>' for item in items)
    st.markdown(f"<div class='card'><h3>{title}</h3><ul class='muted'>{content}</ul></div>", unsafe_allow_html=True)

def callout(text):
    st.markdown(f"<div class='callout'>{text}</div>", unsafe_allow_html=True)

def accent_card(title, text, accent="green"):
    st.markdown(f"<div class='card {accent}'><h3>{title}</h3><p class='muted'>{text}</p></div>", unsafe_allow_html=True)
