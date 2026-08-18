import streamlit as st
from src.data_preparation.clean_data import prepare_data

@st.cache_data
def load_records():
    return prepare_data()

def product_summary(data, product, metric):
    subset = data[data['product'].eq(product)].dropna(subset=[metric]).copy()
    return subset.groupby('governorate', as_index=False)[metric].sum().sort_values(metric, ascending=False)
