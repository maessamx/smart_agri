import streamlit as st
from src.datasets.agriculture.preprocessing import clean_agriculture_data
from src.datasets.agriculture.exploration import product_summary

@st.cache_data
def load_records():
    return clean_agriculture_data()

__all__ = ['load_records', 'product_summary']
