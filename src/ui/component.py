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
    :root{color-scheme:dark;--bg:#0b1411;--surface:#121f1a;--surface-2:#192a23;--border:#294238;--text:#eef7f1;--muted:#a9bdb2;--green:#69c58e;--green-deep:#26724f}
    html,body,[class*="css"]{font-family:"DM Sans",sans-serif;color:var(--text)}
    .stApp{background:radial-gradient(circle at 90% 0,rgba(48,112,78,.16),transparent 28%),var(--bg);color:var(--text)}
    header,footer,#MainMenu{visibility:hidden}.block-container{max-width:1470px;padding-top:1.15rem;padding-bottom:2.5rem}
    h1,h2,h3,h4,h5,h6,p,label,[data-testid="stMarkdownContainer"],.stCaption{color:var(--text)}
    .hero{background:radial-gradient(circle at 85% 15%,rgba(180,217,110,.25),transparent 23%),linear-gradient(120deg,#123c2d,#1d6747 56%,#527d42);border:1px solid rgba(132,207,159,.25);border-radius:25px;padding:2.3rem 2.5rem;color:white;box-shadow:0 14px 38px rgba(0,0,0,.30);margin-bottom:1.2rem}.eyebrow{font-size:.78rem;letter-spacing:2px;font-weight:700;opacity:.82}.hero h1{font-family:"Playfair Display",serif;font-size:2.5rem;margin:.35rem 0;color:#fff}.hero p{max-width:820px;font-size:1.03rem;line-height:1.7;margin:0;opacity:.94;color:#f2f8f4}
    .section-title{font-family:"Playfair Display",serif;color:#8ed6a9;font-size:1.55rem;margin:1.4rem 0 .45rem}.card{height:100%;box-sizing:border-box;background:linear-gradient(145deg,var(--surface-2),var(--surface));border:1px solid var(--border);border-top:4px solid #67b983;border-radius:18px;padding:1.15rem 1.25rem;box-shadow:0 8px 24px rgba(0,0,0,.22)}.card.blue{border-top-color:#62a7d8}.card.gold{border-top-color:#e5a93f}.card.purple{border-top-color:#a58ac8}.card h3{margin:.1rem 0 .5rem;color:#9cddb4}.muted{color:var(--muted);line-height:1.65;font-size:.92rem}.badge{display:inline-block;background:#213d30;color:#9cddb4;border:1px solid #37664d;padding:.25rem .6rem;border-radius:999px;font-size:.76rem;font-weight:700}.top-navigation{font-size:.72rem;letter-spacing:1.5px;color:#9bb4a7;font-weight:700;margin:.1rem 0 .35rem}.callout{background:#162c22;border:1px solid #294d3b;border-left:4px solid #73b88c;border-radius:8px;padding:.8rem 1rem;color:#d8eee0}
    .stButton>button{background:#26724f;color:#fff;border:1px solid #42936b;border-radius:10px;font-weight:700;padding:.56rem .9rem}.stButton>button:hover{background:#328960;color:#fff;border-color:#70c797}.stButton>button:focus{box-shadow:0 0 0 .2rem rgba(105,197,142,.25)}
    [data-testid="stMetric"]{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:.7rem}[data-testid="stMetricLabel"],[data-testid="stMetricValue"],[data-testid="stMetricDelta"]{color:var(--text)}
    [data-baseweb="select"]>div,[data-baseweb="input"]>div,.stTextInput input,.stNumberInput input,.stTextArea textarea{background:var(--surface-2)!important;color:var(--text)!important;border-color:#3b5a4d!important}
    [data-baseweb="popover"],[role="listbox"],[role="option"]{background:var(--surface-2)!important;color:var(--text)!important}[role="option"]:hover,[aria-selected="true"]{background:#28513d!important}
    input,textarea{color:var(--text)!important;caret-color:var(--green)}input::placeholder,textarea::placeholder{color:#8fa69a!important;opacity:1}
    [data-testid="stSlider"] [role="slider"]{background:var(--green)!important}[data-testid="stSlider"] [data-baseweb="slider"]>div>div{background:#39564a}
    [data-testid="stTabs"] [data-baseweb="tab-list"]{gap:.35rem;border-bottom:1px solid var(--border)}[data-testid="stTabs"] button{color:#a9bdb2;background:transparent;border-radius:8px 8px 0 0}[data-testid="stTabs"] button[aria-selected="true"]{color:#8ed6a9;background:#14251e}
    [data-testid="stAlert"]{color:var(--text);border:1px solid rgba(255,255,255,.12)}
    [data-testid="stPageLink-NavLink"]{background:var(--surface);border:1px solid var(--border);border-radius:10px;color:var(--text)}[data-testid="stPageLink-NavLink"]:hover{background:#1d352b;border-color:#46715e;color:#fff}
    [data-testid="stDataFrame"],.stTable{border:1px solid var(--border);border-radius:10px;overflow:hidden}
    code{background:#0a120f;color:#a4e1ba;border:1px solid var(--border);border-radius:5px;padding:.08rem .25rem}hr{border-color:var(--border)}
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
