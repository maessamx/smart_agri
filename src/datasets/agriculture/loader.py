from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[3] / 'data' / 'agriculture' / 'agriculture_governorates_products.csv'


def load_raw_data():
    return pd.read_csv(DATA_PATH)
