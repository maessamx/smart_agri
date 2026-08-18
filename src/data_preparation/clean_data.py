from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[2] / 'data' / 'output2.csv'

def prepare_data():
    data = pd.read_csv(DATA_FILE)
    data = data.replace(['NC', 'N/A', 'UNKNOWN', 'ERROR', ''], pd.NA)
    for column in ['area_feddan', 'production_ton', 'yield_ton_per_feddan']:
        data[column] = pd.to_numeric(data[column], errors='coerce')
    data['year_number'] = data['observation_year'].astype(str).str.extract(r'(\d{4})')[0].astype(float)
    return data
