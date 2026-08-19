import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from .loader import load_raw_data

FEATURES = ['crop ID', 'soil_type', 'Seedling Stage', 'MOI', 'temp', 'humidity']
TARGET = 'result'
CATEGORICAL_COLUMNS = ['crop ID', 'soil_type', 'Seedling Stage']
NUMERIC_COLUMNS = ['MOI', 'temp', 'humidity']
MISSING_MARKERS = ['', 'NC', 'N/A', 'NaN', 'UNKNOWN', 'ERROR']


def clean_irrigation_data(data=None):
    data = load_raw_data() if data is None else data.copy()
    data = data.dropna(how='all').drop_duplicates().reset_index(drop=True)
    data = data.replace(MISSING_MARKERS, pd.NA)
    for column in NUMERIC_COLUMNS + [TARGET]:
        data[column] = pd.to_numeric(data[column], errors='coerce')
    return data.dropna(subset=FEATURES + [TARGET]).reset_index(drop=True)


def build_preprocessor():
    return ColumnTransformer([
        ('categorical', OneHotEncoder(handle_unknown='ignore'), CATEGORICAL_COLUMNS),
        ('numeric', 'passthrough', NUMERIC_COLUMNS)
    ])
