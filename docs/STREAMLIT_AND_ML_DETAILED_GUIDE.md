# Smart Agri Egypt — Streamlit and Machine Learning Reference

This document is a detailed technical reference for maintaining and extending Smart Agri Egypt. It explains the application flow, Streamlit programming patterns, dataset modules, the irrigation machine-learning pipeline, and the purpose of the main parameters used by the project.

---

# Part A — Application Architecture

## A.1 Application flow

The application follows this sequence:

```text
User opens Streamlit application
        ↓
app.py or a file in pages/ is executed
        ↓
initialize_page() loads shared UI and quick navigation
        ↓
Page imports the required dataset module or model module
        ↓
The user selects values or presses a button
        ↓
Streamlit reruns the page from top to bottom
        ↓
The interface shows updated tables, charts, maps, or model output
```

This rerun behavior is the main idea behind Streamlit. A page is not a traditional HTML page with a permanent JavaScript state. It is Python code that is executed again whenever the user interacts with a widget.

## A.2 Source code folders

```text
src/
├── analytics/
│   ├── metrics.py
│   └── charts.py
├── datasets/
│   ├── agriculture/
│   └── irrigation/
├── geo_service.py
└── ui/
    └── component.py
```

### `src/analytics/`

Contains reusable analysis helpers:

- `metrics.py`: one shared dictionary that maps labels such as `Production` to real dataframe columns such as `production_ton`.
- `charts.py`: reusable Matplotlib and Plotly chart functions.

This avoids writing the same chart structure or metric mapping in several places.

### `src/datasets/`

Contains one module per dataset. Each dataset has its own rules because agricultural product data and irrigation model data do not have the same columns or preprocessing requirements.

### `src/ui/component.py`

Contains shared CSS and reusable user-interface functions. Pages call the functions instead of repeating HTML and CSS.

---

# Part B — Streamlit Step by Step

## B.1 Create a basic page

```python
import streamlit as st

st.set_page_config(
    page_title="Example Page",
    page_icon="🌱",
    layout="wide"
)

st.title("Example Page")
st.write("This is a Streamlit page.")
```

Run the application:

```bash
streamlit run app.py
```

## B.2 Use the project shared interface

Every project page should start with:

```python
import streamlit as st
from src.ui.component import initialize_page, hero

st.set_page_config(
    page_title="New Feature | Smart Agri Egypt",
    page_icon="🌱",
    layout="wide"
)

initialize_page()
hero(
    "New Feature",
    "Short description of the feature."
)
```

`initialize_page()` applies the shared CSS and shows the quick-navigation links. This keeps pages consistent.

## B.3 Text components

```python
st.title("Main Title")
st.header("Header")
st.subheader("Subheader")
st.write("Normal text")
st.caption("Small supporting text")
st.markdown("**Bold markdown text**")
```

## B.4 Columns

```python
left, right = st.columns(2)

with left:
    st.write("Left content")

with right:
    st.write("Right content")
```

Use columns for dashboards, filters, metrics, and grouped controls.

## B.5 Metrics

```python
col1, col2, col3 = st.columns(3)
col1.metric("Cultivated Area", "5,000 feddan")
col2.metric("Production", "15,000 tons")
col3.metric("Yield", "3.0 t/feddan")
```

## B.6 Input widgets

### Dropdown

```python
crop = st.selectbox(
    "Select Crop",
    ["Wheat", "Rice", "Tomato"]
)
```

### Numeric input

```python
area = st.number_input(
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

### Radio selection

```python
metric = st.radio(
    "Metric",
    ["Production", "Cultivated Area", "Yield"],
    horizontal=True
)
```

## B.7 Buttons

```python
if st.button("Run Analysis"):
    st.success("Analysis started")
```

A button returns `True` only during the rerun caused by that button click.

## B.8 A button that calls a function in the same file

```python
def calculate_production(area, yield_per_feddan):
    return area * yield_per_feddan

area = st.number_input("Area", min_value=0.1)

if st.button("Calculate"):
    result = calculate_production(area, 3.2)
    st.write(f"Expected production: {result:.2f} tons")
```

## B.9 A button that calls a function in another file

Create a function in a separate module:

```python
# src/services/production_service.py

def calculate_production(area, yield_per_feddan):
    return area * yield_per_feddan
```

Import it in a page:

```python
from src.services.production_service import calculate_production

if st.button("Calculate"):
    result = calculate_production(area, 3.2)
    st.write(result)
```

This is preferred when the function may be used by multiple pages.

## B.10 Create a new page

Create a file inside `pages/`:

```text
pages/7_Weather_Monitoring.py
```

Example:

```python
import streamlit as st
from src.ui.component import initialize_page, hero, text_card

st.set_page_config(
    page_title="Weather Monitoring | Smart Agri Egypt",
    page_icon="☀️",
    layout="wide"
)

initialize_page()
hero("Weather Monitoring", "Weather information for farm planning.")
text_card("Future Integration", "Weather API data will be displayed here.")
```

Then add its link inside `render_top_navigation()` in:

```text
src/ui/component.py
```

---

# Part C — Data Modules and Preprocessing

## C.1 Why modules are used

The project keeps every dataset separate because each one has different columns, cleaning rules, and future models.

```text
src/datasets/
├── agriculture/
│   ├── loader.py
│   ├── preprocessing.py
│   └── exploration.py
└── irrigation/
    ├── loader.py
    ├── preprocessing.py
    ├── exploration.py
    └── model.py
```

## C.2 Agricultural dataset flow

Source file:

```text
data/agriculture/agriculture_governates_products.csv
```

### Loading

```python
from src.datasets.agriculture.loader import load_raw_data

data = load_raw_data()
```

### Cleaning

```python
from src.datasets.agriculture.preprocessing import clean_agriculture_data

clean_data = clean_agriculture_data()
```

Cleaning steps:

1. Remove completely empty rows.
2. Remove duplicate rows.
3. Replace text markers such as `NC`, `N/A`, and `UNKNOWN` with missing values.
4. Convert area, production, and yield columns to numeric types.
5. Extract a numerical year from `observation_year`.

## C.3 Irrigation dataset flow

Source file:

```text
data/irrigation/irrigation_training_data.csv
```

The dataset includes:

| Column | Type | Meaning |
|---|---|---|
| `crop ID` | Categorical | Crop name such as Wheat or Tomato. |
| `soil_type` | Categorical | Soil classification. |
| `Seedling Stage` | Categorical | Current crop growth stage. |
| `MOI` | Numeric | Moisture index. |
| `temp` | Numeric | Temperature. |
| `humidity` | Numeric | Relative humidity. |
| `result` | Target | Irrigation class. |

### Cleaning code pattern

```python
data = data.dropna(how="all")
data = data.drop_duplicates()
data = data.replace(["", "NC", "N/A"], pd.NA)
```

### Numeric conversion

```python
for column in ["MOI", "temp", "humidity", "result"]:
    data[column] = pd.to_numeric(data[column], errors="coerce")
```

`errors="coerce"` means invalid text values become `NaN` instead of causing the application to stop.

### Final record selection

```python
data = data.dropna(subset=FEATURES + [TARGET])
```

This ensures that the machine-learning model only trains on rows that contain all required input features and the target label.

---

# Part D — Machine Learning Pipeline

## D.1 Model purpose

The irrigation model classifies a farm condition into one of three project decision classes:

| Class | Application meaning |
|---:|---|
| 0 | No irrigation required |
| 1 | Medium irrigation required |
| 2 | High irrigation required |

## D.2 Features and target

```python
FEATURES = [
    "crop ID",
    "soil_type",
    "Seedling Stage",
    "MOI",
    "temp",
    "humidity"
]

TARGET = "result"
```

- Features are the inputs given to the model.
- Target is the label that the model learns to predict.

## D.3 Why categorical preprocessing is needed

A model cannot use words such as `Wheat`, `Clay Soil`, or `Flowering` directly. They must be transformed into numeric features.

The project uses:

```python
OneHotEncoder(handle_unknown="ignore")
```

Example concept:

```text
Crop ID = Wheat
```

can become:

```text
Wheat = 1
Tomato = 0
Potato = 0
Chilli = 0
```

### `handle_unknown="ignore"`

If the user enters a new categorical value that was not seen during training, the application does not crash. It ignores the unknown category instead.

## D.4 ColumnTransformer

The project has both categorical and numeric inputs. `ColumnTransformer` applies different transformations to each group.

```python
ColumnTransformer([
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

### Categorical branch

```python
OneHotEncoder(...)
```

Converts text values into numeric columns.

### Numeric branch

```python
"passthrough"
```

Keeps `MOI`, `temp`, and `humidity` as numeric values without changing them.

## D.5 Pipeline

A `Pipeline` combines preprocessing and model training in one object.

```python
Pipeline([
    ("preprocessor", build_preprocessor()),
    ("classifier", RandomForestClassifier(...))
])
```

The pipeline guarantees that:

1. Training data is encoded correctly.
2. New user input is encoded in exactly the same way.
3. The classifier receives correctly formatted features.

---

# Part E — Random Forest Classifier

## E.1 What is Random Forest?

Random Forest is an ensemble model. Instead of relying on one decision tree, it creates many decision trees and combines their decisions.

```text
Input data
   ↓
Decision Tree 1
Decision Tree 2
Decision Tree 3
...
Decision Tree 300
   ↓
Majority vote
   ↓
Final class
```

It is useful here because it can handle:

- Numeric data.
- Encoded categorical data.
- Non-linear relationships.
- Multiple input features.
- Different crop and soil combinations.

## E.2 Random Forest parameters used

```python
RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)
```

### `n_estimators=300`

This is the number of decision trees in the forest.

```text
300 trees
```

More trees usually improve stability, but also increase training time. Three hundred trees is a practical balance for this dataset.

### `random_state=42`

This fixes the random seed.

Why it matters:

- The model can be reproduced.
- The train/test split can be reproduced.
- Different team members obtain the same result using the same data and code.

The number `42` is not mathematically special. Any fixed integer could be used.

### `n_jobs=-1`

This tells scikit-learn to use all available processor cores during training.

Benefits:

- Faster training.
- Useful for Random Forest because many trees can train in parallel.

## E.3 Train-test split

The project evaluates the model before building the final deployed version.

```python
x_train, x_test, y_train, y_test = train_test_split(
    features,
    target,
    test_size=0.20,
    random_state=42,
    stratify=target
)
```

### `test_size=0.20`

Uses 20% of records for testing and 80% for training.

```text
80% → Training
20% → Testing
```

### `stratify=target`

Keeps the class proportions similar in training and testing datasets.

If class 0, 1, and 2 are not equally common, stratification prevents a split where one class is underrepresented in the testing data.

## E.4 Accuracy

```python
accuracy = accuracy_score(y_test, predictions)
```

Accuracy is:

```text
correct predictions / total test predictions
```

The application displays validation accuracy in the Irrigation Control page. Accuracy is useful as a basic measure, but a production system should later also use:

- Precision.
- Recall.
- F1-score.
- Confusion matrix.
- Field validation.

## E.5 Deployment model

After evaluation, the application fits a final model on the complete cleaned dataset:

```python
deployment_model.fit(features, target)
```

Why:

- The final model can learn from all available valid records.
- The test split is used for evaluation, not wasted after evaluation.

## E.6 Prediction probability and confidence

```python
probabilities = model.predict_proba(input_data)[0]
confidence = probabilities.max()
```

Example:

```text
Class 0 probability = 0.03
Class 1 probability = 0.91
Class 2 probability = 0.06
```

The predicted class is:

```text
Class 1
```

The confidence shown is:

```text
91%
```

Confidence is not a guarantee of correctness. It only indicates how strongly the model prefers one class compared with the other classes.

## E.7 Triggering a prediction with a Streamlit button

```python
if st.button("Evaluate Irrigation Requirement"):
    input_data = pd.DataFrame([{
        "crop ID": crop,
        "soil_type": soil,
        "Seedling Stage": stage,
        "MOI": moisture,
        "temp": temperature,
        "humidity": humidity
    }])

    predicted_class, confidence = predict(input_data)
```

The button controls when the model inference is displayed. The trained model itself is cached using `@st.cache_resource`, so it does not need to train again on every click.

---

# Part F — Graphs and Maps

## F.1 Plotly bar chart

```python
figure = px.bar(
    summary,
    x="production_ton",
    y="governorate",
    orientation="h",
    color="production_ton"
)

st.plotly_chart(figure, use_container_width=True)
```

Use Plotly when the user needs hover tooltips, zoom, download options, or interactive filtering.

## F.2 Matplotlib chart

```python
figure, axis = plt.subplots(figsize=(10, 6))
axis.barh(summary["governorate"], summary["production_ton"])
axis.set_xlabel("Production (tons)")

st.pyplot(figure, use_container_width=True)
```

Use Matplotlib for report-like static charts with fine visual control.

## F.3 Stacked bar chart

```python
grouped = data.groupby(
    ["governorate", "product_category"],
    as_index=False
)["area_feddan"].sum()

figure = px.bar(
    grouped,
    x="governorate",
    y="area_feddan",
    color="product_category",
    barmode="stack"
)
```

Each governorate becomes one column. Each colored section represents a product category.

## F.4 Folium GeoJSON map

```python
geojson = load_governorate_geojson()

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

The `key_on` value is important. It connects the governorate name inside the GeoJSON geometry to the governorate name in the dataframe.

---

# Part G — Development Checklist

Before adding a new feature, ask:

1. Is there a new dataset? Create a new folder in `data/` and a new module in `src/datasets/`.
2. Is there repeated user-interface code? Add a reusable function to `src/ui/component.py`.
3. Is there repeated chart logic? Add a function to `src/analytics/charts.py`.
4. Is there repeated metric mapping? Add it to `src/analytics/metrics.py`.
5. Is there a new ML model? Keep it inside its own dataset module under `model.py`.
6. Does the page need a new link? Update `render_top_navigation()`.
7. Does the page need a new dependency? Add it to `requirements.txt`.
8. Did the change run without errors? Test the page before committing.

---

# Part H — Safety Note

The irrigation model is a training-project decision-support component. Model predictions must not directly control pumps, valves, or fertilizer dosing without calibrated sensors, field validation, safety limits, and human approval.
