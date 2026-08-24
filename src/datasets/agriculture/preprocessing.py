import pandas as pd
from .loader import load_raw_data

MISSING_MARKERS = ['', 'NC', 'N/A', 'NaN', 'UNKNOWN', 'ERROR']
NUMERIC_COLUMNS = ['area_feddan', 'production_ton', 'yield_ton_per_feddan']


def clean_agriculture_data(data=None):
    data = load_raw_data() if data is None else data.copy()
    data = data.dropna(how='all').drop_duplicates().reset_index(drop=True)
    data = data.replace(MISSING_MARKERS, pd.NA)
    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors='coerce')
    data['year_number'] = data['observation_year'].astype(str).str.extract(r'(\d{4})')[0].astype(float)
    return data
