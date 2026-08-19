# Data Module Architecture

The project uses a dataset-centered module structure. Each dataset has its own loader, preprocessing logic, exploration functions, and model logic where required.

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

## Agriculture Dataset

Source: `data/agriculture/agriculture_governorates_products.csv`

- `loader.py`: reads the source CSV.
- `preprocessing.py`: removes duplicate/empty rows, standardizes missing markers, converts agricultural metrics into numeric values, and extracts the reference year.
- `exploration.py`: provides dataset overview and governorate-level product aggregation.

## Irrigation Dataset

Source: `data/irrigation/irrigation_training_data.csv`

- `loader.py`: reads irrigation training data.
- `preprocessing.py`: removes duplicate rows, handles missing values, converts numeric columns, defines the feature groups, and creates the OneHotEncoder preprocessing pipeline.
- `exploration.py`: returns class distribution and descriptive numeric statistics.
- `model.py`: trains and caches the Random Forest classification model, then exposes prediction functions to the irrigation page.

This structure makes it possible to add future datasets such as fertilizer, weather, or production forecasting without mixing their processing rules with existing modules.
