# Streamlit Development Guide

This guide explains the Streamlit concepts used in Smart Agri Egypt and provides patterns for extending the project.

## 1. Basic Application File

A Streamlit application is a Python file. The root file in this project is `app.py`.

```python
import streamlit as st

st.set_page_config(
    page_title="Smart Agri Egypt",
    page_icon="🌿",
    layout="wide"
)

st.title("Smart Agri Egypt")
st.write("Agricultural analytics dashboard")
```

Run it using:

```bash
streamlit run app.py
```

## 2. Layout Components

### Text

```python
st.title("Main Title")
st.header("Header")
st.subheader("Subheader")
st.write("Normal text")
st.caption("Secondary text")
st.markdown("**Bold text**")
```

### Columns

```python
left, right = st.columns(2)

with left:
    st.metric("Production", "12,500 tons")

with right:
    st.metric("Yield", "3.2 t/feddan")
```

### Containers

```python
with st.container(border=True):
    st.subheader("Card Content")
    st.write("Grouped content")
```

## 3. Buttons and Functions

A button returns `True` only when pressed during the current run.

```python
if st.button("Calculate"):
    result = 10 * 5
    st.success(f"Result: {result}")
```

To call a separate function:

```python
def calculate_yield(area, yield_per_feddan):
    return area * yield_per_feddan

area = st.number_input("Area", min_value=0.0)
if st.button("Estimate Production"):
    production = calculate_yield(area, 3.2)
    st.write(production)
```

## 4. Input Widgets

```python
crop = st.selectbox("Crop", ["Wheat", "Rice", "Tomato"])
area = st.number_input("Farm area", min_value=0.1, value=1.0)
moisture = st.slider("Soil moisture", 0, 100, 45)
use_weather = st.checkbox("Use weather adjustment")
```

## 5. Session State

`st.session_state` stores information between reruns.

```python
if "selected_crop" not in st.session_state:
    st.session_state.selected_crop = "Wheat"

if st.button("Select Rice"):
    st.session_state.selected_crop = "Rice"

st.write(st.session_state.selected_crop)
```

Use session state for temporary user selections, form state, login state, or multi-step workflows.

## 6. Multi-Page Applications

Streamlit automatically detects Python files placed in the `pages/` folder.

```text
pages/
├── 1_Project_Brief.py
├── 2_Crop_Intelligence.py
└── 3_Analytics_Studio.py
```

The numeric prefix controls page order.

### Page links

Use `st.page_link()` to create navigation links.

```python
st.page_link(
    "pages/2_Crop_Intelligence.py",
    label="Crop Intelligence",
    icon="🌱"
)
```

In this project, shared navigation is implemented once in:

```text
src/ui/component.py
```

## 7. Shared UI Components

Reusable components prevent repeated HTML, CSS, and layout code.

Example component:

```python
def info_card(title, text, icon=None):
    icon_html = f"<div>{icon}</div>" if icon else ""
    st.markdown(
        f"<div class='card'>{icon_html}<h3>{title}</h3><p>{text}</p></div>",
        unsafe_allow_html=True
    )
```

Use it in a page:

```python
from src.ui.component import info_card

info_card(
    "Crop Intelligence",
    "Compare crop performance across governorates.",
    "🌱"
)
```

The project uses these shared components:

- `initialize_page()` — loads global UI style and quick navigation.
- `hero()` — page hero section.
- `section_title()` — unified section heading.
- `info_card()` — feature card.
- `text_card()` — text card.
- `bullet_card()` — bullet-list card.
- `callout()` — highlighted information message.
- `coming_soon()` — standardized reserved module page.

## 8. Data Loading and Caching

Use `st.cache_data` for data that should not be loaded again every rerun.

```python
@st.cache_data
def load_data():
    return pd.read_csv("data/agriculture/agriculture_governorates_products.csv")

data = load_data()
```

In this project, the preparation logic is separated into:

```text
src/data_preparation/clean_data.py
```

and data access is handled by:

```text
src/data_service.py
```

## 9. Pandas Filtering and Aggregation

### Filter

```python
selected = data[data["product"].eq("Wheat Grain")]
```

### Group by governorate

```python
summary = (
    selected
    .groupby("governorate", as_index=False)["production_ton"]
    .sum()
    .sort_values("production_ton", ascending=False)
)
```

## 10. Plotly Charts

### Bar Chart

```python
import plotly.express as px

fig = px.bar(
    summary,
    x="production_ton",
    y="governorate",
    orientation="h"
)
st.plotly_chart(fig, use_container_width=True)
```

### Stacked Bar Chart

```python
summary = data.groupby(
    ["governorate", "product_category"],
    as_index=False
)["area_feddan"].sum()

fig = px.bar(
    summary,
    x="governorate",
    y="area_feddan",
    color="product_category",
    barmode="stack"
)
st.plotly_chart(fig, use_container_width=True)
```

## 11. Matplotlib Charts

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(summary["governorate"], summary["production_ton"])
ax.set_xlabel("Production (tons)")
ax.set_ylabel("Governorate")
st.pyplot(fig, use_container_width=True)
```

Use Matplotlib when you want a controlled static chart suitable for reports and presentations.

## 12. Folium Maps

### Create a map

```python
import folium
from streamlit_folium import st_folium

fmap = folium.Map(location=[27.2, 30.8], zoom_start=5)
```

### Add a marker

```python
folium.Marker(
    location=[30.0, 31.0],
    popup="Cairo"
).add_to(fmap)
```

### Add a Choropleth GeoJSON layer

```python
folium.Choropleth(
    geo_data=geojson,
    data=summary,
    columns=["governorate", "production_ton"],
    key_on="feature.properties.governorate",
    fill_color="YlGn"
).add_to(fmap)
```

### Show the map in Streamlit

```python
st_folium(fmap, height=570, use_container_width=True)
```

## 13. Recommended Pattern for New Features

For a new module such as notifications:

1. Create a page inside `pages/`.
2. Start it with `initialize_page()`.
3. Keep repeated visual elements inside `src/ui/component.py`.
4. Put cleaning and transformations inside `src/data_preparation/`.
5. Put reusable data queries inside `src/data_service.py`.
6. Keep the page file focused on user interactions and presentation only.

Example:

```python
import streamlit as st
from src.ui.component import initialize_page, hero, section_title

st.set_page_config(layout="wide")
initialize_page()
hero("Notifications", "Farm notifications and alerts.")
section_title("Recent Alerts")
st.info("No alerts available.")
```

## 14. Practical Development Tips

- Use one function for every repeated calculation.
- Use one shared component for every repeated visual block.
- Avoid mixing data cleaning with page layout code.
- Use clear column names and keep metric units visible.
- Use `st.cache_data` for CSV loading and remote GeoJSON requests.
- Test every page after adding a new feature.
- Add error handling for unavailable data or network services.
