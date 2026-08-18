# Smart Agri Egypt

## Summer Training Project

**Faculty of Engineering — Capital University**  
**Computer and Systems Engineering Department**

**Team Members**
- Mahmoud Essam
- Karim Arafat
- Youssef Hegazy
- Youssef Mohamed
- Youssef Farag

## Overview

Smart Agri Egypt is a data-driven agricultural dashboard developed as a summer training project. The platform presents agricultural information for Egypt’s governorates through an organized interactive interface. It supports crop exploration, product comparison, geographic visualization, and analytical charts.

The system is designed as a foundation for a broader smart agriculture platform that can later incorporate soil sensors, irrigation monitoring, nutrient tracking, yield forecasting, weather integration, and farm notifications.

## Main Features

- Comparison of 30 common agricultural products across 27 Egyptian governorates.
- Crop ranking within a selected governorate.
- National ranking of governorates for a selected product.
- Interactive Folium GeoJSON map for product distribution.
- Matplotlib governorate comparison chart.
- Stacked bar chart for category composition by governorate.
- Academic project presentation page.
- Reserved modules for irrigation, fertilizer management, and yield forecasting.

## Dataset

The project uses one local dataset:

```text
data/output2.csv
```

It contains governorate-level records for crops, cultivated area, production, yield, crop category, observation year, and season type.

## Technologies

- Python
- Streamlit
- Pandas
- Folium
- streamlit-folium
- Matplotlib
- Plotly

## Repository Structure

```text
smart_agri_egypt/
├── app.py
├── pages/
├── src/
│   ├── ui/
│   └── data_preparation/
├── data/
├── notebooks/
├── assets/
└── docs/
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd smart_agri_egypt
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application opens through the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Notes

The GeoJSON governorate boundary layer is loaded dynamically using the ArcGIS endpoint documented in the analysis notebook. The local project stores only the provided agricultural dataset.
