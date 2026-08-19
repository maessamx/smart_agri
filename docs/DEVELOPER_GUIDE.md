# Smart Agri Egypt — Developer Guide

This guide explains how the project is structured and how to extend it step by step. It is written for the project team so that new features can be added without mixing interface code, data logic, and machine-learning code.

---

## 1. Project Overview

Smart Agri Egypt is a Streamlit application built around three main ideas:

1. **Agricultural analytics**: compare crops, area, production, and yield across Egyptian governorates.
2. **Irrigation decision support**: use a trained classification model to classify irrigation needs.
3. **Scalable architecture**: keep each dataset, model, page, and shared interface element in a separate location.

The application starts from:

```text
app.py
```

Run the application with:

```bash
streamlit run app.py
```

---

## 2. Project Structure

```text
smart_agri/
├── app.py
├── config.py
├── requirements.txt
│
├── pages/
│   ├── 1_Project_Brief.py
│   ├── 2_Crop_Intelligence.py
│   ├── 4_Irrigation_Control.py
│   ├── 5_Fertilizer_Recommendation.py
│   └── 6_Production_Forecast.py
│
├── data/
│   ├── agriculture/
│   │   └── agriculture_governates_products.csv
│   └── irrigation/
│       └── irrigation_training_data.csv
│
├── src/
│   ├── datasets/
│   │   ├── agriculture/
│   │   └── irrigation/
│   ├── geo_service.py
│   └── ui/
│       └── component.py
│
├── notebooks/
├── docs/
└── assets/
```

### Responsibilities

| Location | Responsibility |
|---|---|
| `pages/` | User-facing Streamlit pages. |
| `data/` | Source datasets only. |
| `src/datasets/` | Loading, cleaning, exploring, and modeling each dataset. |
| `src/ui/component.py` | Shared CSS, navigation, cards, headings, and reusable interface components. |
| `src/geo_service.py` | Dynamic loading and name matching for governorate GeoJSON geometry. |
| `notebooks/` | Exploratory analysis and model experiments. |
| `docs/` | Project documentation. |

---

## 3. How Streamlit Works

A Streamlit page is a Python file that runs from top to bottom every time the user changes an input, presses a button, or opens a page.

Simple example:

```python
import streamlit as st

st.title("Smart Agri Egypt")
st.write("Agricultural decision support dashboard")
```

When the browser opens the application, Streamlit runs this code and converts the output into a web interface.

### Page configuration

Use `st.set_page_config()` before creating any visual element:

```python
st.set_page_config(
    page_title="Crop Intelligence | Smart Agri Egypt",
    page_icon="🌱",
    layout="wide"
)
```

- `page_title`: browser tab title.
- `page_icon`: browser tab icon.
- `layout="wide"`: uses the available screen width.

---

## 4. Shared Components

The project does not repeat design code in every page. Shared elements are stored in:

```text
src/ui/component.py
```

Each page begins with:

```python
from src.ui.component import initialize_page, hero

initialize_page()
hero(
    "Crop Intelligence",
    "Compare products and identify leading cultivation locations."
)
```

### `initialize_page()`

This function automatically:

1. Loads the common CSS.
2. Displays Quick Navigation.
3. Keeps every page visually consistent.

### Available shared components

```python
hero(title, text)
section_title(title)
info_card(title, text, icon)
text_card(title, text)
bullet_card(title, items)
accent_card(title, text, accent)
callout(text)
coming_soon(title, text)
```

### Example: showing a colored card

```python
from src.ui.component import accent_card

accent_card(
    "Solution",
    "An interactive dashboard for agricultural analytics.",
    "blue"
)
```

Available accent colors currently include:

```text
green
blue
gold
purple
```

---

## 5. Creating a New Page

Streamlit treats files inside `pages/` as application pages.

### Step 1: create a new file

For example:

```text
pages/7_Weather_Monitoring.py
```

The numeric prefix controls the page order.

### Step 2: add page code

```python
import streamlit as st
from src.ui.component import initialize_page, hero, section_title, text_card

st.set_page_config(
    page_title="Weather Monitoring | Smart Agri Egypt",
    page_icon="☀️",
    layout="wide"
)

initialize_page()

hero(
    "Weather Monitoring",
    "Current and historical weather conditions for agricultural planning."
)

section_title("Weather Summary")
text_card(
    "Future Module",
    "Weather data and forecasts will be connected here."
)
```

### Step 3: add the page to Quick Navigation

Open:

```text
src/ui/component.py
```

Add a link inside `render_top_navigation()`:

```python
weather.page_link(
    "pages/7_Weather_Monitoring.py",
    label="Weather",
    icon="☀️"
)
```

---

## 6. Displaying Text, Messages, and Metrics

### Basic text

```python
st.title("Main Title")
st.header("Header")
st.subheader("Subheader")
st.write("Normal text")
st.caption("Small helper text")
st.markdown("**Bold text**")
```

### Status messages

```python
st.success("Operation completed successfully")
st.info("Additional information")
st.warning("Check this input")
st.error("An error occurred")
```

### Metrics

```python
col1, col2, col3 = st.columns(3)

col1.metric("Production", "15,000 tons")
col2.metric("Area", "5,000 feddan")
col3.metric("Yield", "3.0 t/feddan")
```

---

## 7. Input Widgets

Widgets allow users to interact with the application.

### Selectbox

```python
crop = st.selectbox(
    "Select Crop",
    ["Wheat", "Rice", "Tomato"]
)
```

The selected value is stored in `crop`.

### Number input

```python
farm_area = st.number_input(
    "Farm Area (feddan)",
    min_value=0.1,
    value=5.0,
    step=0.5
)
```

### Slider

```python
moisture = st.slider(
    "Soil Moisture (%)",
    min_value=0,
    max_value=100,
    value=40
)
```

### Radio buttons

```python
metric = st.radio(
    "Select Metric",
    ["Production", "Area", "Yield"],
    horizontal=True
)
```

---

## 8. Buttons and Functions

A Streamlit button returns `True` only when the user presses it.

```python
if st.button("Calculate"):
    st.success("Calculation started")
```

### Calling a function in the same file

```python
def estimate_production(area, yield_per_feddan):
    return area * yield_per_feddan

area = st.number_input("Area", min_value=0.1)

if st.button("Estimate Production"):
    result = estimate_production(area, 3.2)
    st.write(f"Expected production: {result:.2f} tons")
```

### Calling a function from another file

Create a service file:

```python
# src/services/forecast_service.py

def estimate_production(area, yield_per_feddan):
    return area * yield_per_feddan
```

Import it in a page:

```python
from src.services.forecast_service import estimate_production

if st.button("Estimate Production"):
    result = estimate_production(area, 3.2)
    st.write(result)
```

This pattern keeps the page focused on interface logic and keeps calculations in reusable modules.

---

## 9. Loading and Preprocessing Data

### Agricultural data

The source file is:

```text
data/agriculture/agriculture_governates_products.csv
```

The loading path is:

```text
src/datasets/agriculture/loader.py
```

The cleaning logic is:

```text
src/datasets/agriculture/preprocessing.py
```

Example cleaning process:

```python
def clean_agriculture_data(data=None):
    data = load_raw_data() if data is None else data.copy()
    data = data.dropna(how="all").drop_duplicates()
    data = data.replace(["", "NC", "N/A"], pd.NA)

    for column in [
        "area_feddan",
        "production_ton",
        "yield_ton_per_feddan"
    ]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    return data
```

### Why preprocessing is separated

Preprocessing should not be written directly in page files because it may be needed by multiple pages. A separate module makes the code reusable and easier to test.

---

## 10. Caching Data

Streamlit reruns a page frequently. Reading a CSV or training a model every time can make the application slow.

### Cache data

```python
@st.cache_data
def load_records():
    return clean_agriculture_data()
```

Use `@st.cache_data` for:

- CSV files.
- JSON files.
- DataFrames.
- API responses.
- Aggregated results.

### Cache models

```python
@st.cache_resource
def train_model():
    model.fit(X_train, y_train)
    return model
```

Use `@st.cache_resource` for:

- Machine-learning models.
- Database connections.
- Heavy resources.

---

## 11. Irrigation Model Workflow

The irrigation model uses:

```text
data/irrigation/irrigation_training_data.csv
```

### Features

```python
FEATURES = [
    "crop ID",
    "soil_type",
    "Seedling Stage",
    "MOI",
    "temp",
    "humidity"
]
```

### Target

```python
TARGET = "result"
```

### Preprocessing pipeline

Categorical columns are encoded using `OneHotEncoder`:

```python
preprocessor = ColumnTransformer([
    (
        "categorical",
        OneHotEncoder(handle_unknown="ignore"),
        CATEGORICAL_COLUMNS
    ),
    (
        "numeric",
        "passthrough",
        NUMERIC_COLUMNS
    )
])
```

### Model training

```python
model = Pipeline([
    ("preprocessor", preprocessor),
    (
        "classifier",
        RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            n_jobs=-1
        )
    )
])

model.fit(data[FEATURES], data[TARGET])
```

### Train the model with a button

Normally, the model is loaded from cache in this project. If a future page needs a training button, the pattern is:

```python
from src.datasets.irrigation.model import train_model

if st.button("Train Irrigation Model"):
    with st.spinner("Training model..."):
        model, training_data = train_model()
    st.success("Model training completed")
```

### Make a prediction

```python
from src.datasets.irrigation.model import predict

input_data = pd.DataFrame([{
    "crop ID": "Wheat",
    "soil_type": "Clay Soil",
    "Seedling Stage": "Flowering",
    "MOI": 20,
    "temp": 35,
    "humidity": 50
}])

predicted_class, confidence = predict(input_data)
```

Current interface interpretation:

| Predicted Class | Decision |
|---:|---|
| 0 | No irrigation required |
| 1 | Medium irrigation required |
| 2 | High irrigation required |

---

## 12. Pandas Analysis Examples

### Filter by product

```python
wheat_data = records[
    records["product"].eq("Wheat Grain")
]
```

### Aggregate production by governorate

```python
summary = (
    wheat_data
    .dropna(subset=["production_ton"])
    .groupby("governorate", as_index=False)["production_ton"]
    .sum()
    .sort_values("production_ton", ascending=False)
)
```

### Get the top governorate

```python
top_governorate = summary.iloc[0]

st.success(
    f"{top_governorate['governorate']} ranks first"
)
```

---

## 13. Plotly Charts

### Horizontal bar chart

```python
import plotly.express as px

figure = px.bar(
    summary.head(15),
    x="production_ton",
    y="governorate",
    orientation="h",
    color="production_ton",
    color_continuous_scale="YlGn"
)

st.plotly_chart(figure, use_container_width=True)
```

### Stacked bar chart

```python
grouped = (
    records
    .groupby(
        ["governorate", "product_category"],
        as_index=False
    )["area_feddan"]
    .sum()
)

figure = px.bar(
    grouped,
    x="governorate",
    y="area_feddan",
    color="product_category",
    barmode="stack"
)

st.plotly_chart(figure, use_container_width=True)
```

---

## 14. Matplotlib Charts

```python
import matplotlib.pyplot as plt

figure, axis = plt.subplots(figsize=(10, 6))
axis.barh(
    summary["governorate"],
    summary["production_ton"],
    color="#25734D"
)
axis.set_xlabel("Production (tons)")
axis.set_ylabel("Governorate")
axis.grid(axis="x", alpha=0.18)

st.pyplot(figure, use_container_width=True)
```

Matplotlib is useful for charts that need a fixed, report-like design.

---

## 15. Folium and GeoJSON Maps

The project loads Egyptian governorate geometry dynamically in:

```text
src/geo_service.py
```

### Load GeoJSON

```python
geojson = load_governorate_geojson()
```

### Create a Choropleth map

```python
fmap = folium.Map(
    location=[27.2, 30.8],
    zoom_start=5,
    tiles="CartoDB positron"
)

folium.Choropleth(
    geo_data=geojson,
    data=summary,
    columns=["governorate", "area_feddan"],
    key_on="feature.properties.governorate",
    fill_color="YlGn",
    fill_opacity=0.80,
    line_opacity=0.35
).add_to(fmap)

st_folium(fmap, height=570, use_container_width=True)
```

The map colors each governorate according to the selected metric.

---

## 16. Adding a Future Fertilizer Module

Recommended structure:

```text
src/datasets/fertilizer/
├── loader.py
├── preprocessing.py
├── exploration.py
└── model.py
```

Possible inputs:

```text
Crop type
N reading
P reading
K reading
Soil pH
Farm area
Growth stage
```

Possible output:

```text
Fertilizer type
Recommended quantity
Application timing
Safety message
```

---

## 17. Adding a Future Production Forecast Module

Recommended structure:

```text
src/datasets/production/
├── loader.py
├── preprocessing.py
├── feature_engineering.py
└── model.py
```

Possible inputs:

```text
Crop type
Governorate
Farm area
Historical yield
Soil moisture
NPK
Temperature
Humidity
Season
```

Possible output:

```text
Expected production in tons
Minimum estimate
Maximum estimate
Key factors affecting the result
```

---

## 18. Recommended Development Rules

1. Keep source data inside `data/`.
2. Keep cleaning logic inside `src/datasets/<dataset>/preprocessing.py`.
3. Keep ML training and inference inside `src/datasets/<dataset>/model.py`.
4. Keep page files focused on user interface and user interaction.
5. Keep shared CSS and reusable cards inside `src/ui/component.py`.
6. Use a separate page for each major feature.
7. Use cached functions for files, API calls, and trained models.
8. Test a page after every major change.
9. Keep units visible: feddan, tons, tons/feddan, percentages, and degrees Celsius.
10. Do not treat a model result as a physical irrigation command without field validation and safety rules.
