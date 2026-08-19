import math
import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium
from src.geo_service import load_governorate_geojson
from src.data_service import load_records, product_summary
from src.analytics.metrics import METRICS, metric_column
from src.analytics.charts import governorate_ranking_chart, stacked_category_chart
from src.ui.component import initialize_page, hero, callout

st.set_page_config(page_title='Crop Intelligence | Smart Agri Egypt', page_icon='🌱', layout='wide', initial_sidebar_state='expanded')
initialize_page()
records = load_records()
hero('Crop Intelligence', 'Compare products within a governorate, find the strongest cultivation locations in Egypt, and explore the selected product on an interactive map.')

def valid(data):
    return data.dropna(subset=['area_feddan', 'production_ton'], how='all').copy()

def build_map(summary, product, metric):
    fmap = folium.Map(location=[27.2, 30.8], zoom_start=5, tiles='CartoDB positron', control_scale=True)
    try:
        geojson = load_governorate_geojson()
        folium.Choropleth(
            geo_data=geojson,
            data=summary,
            columns=['governorate', metric],
            key_on='feature.properties.governorate',
            fill_color='YlGn',
            fill_opacity=.80,
            line_opacity=.35,
            nan_fill_color='#E5E7EB',
            legend_name=f'{product} — {metric.replace("_", " ").title()}'
        ).add_to(fmap)
        folium.GeoJsonTooltip(
            fields=['governorate'],
            aliases=['Governorate:'],
            sticky=False
        ).add_to(folium.GeoJson(geojson).add_to(fmap))
    except Exception:
        st.warning('The governorate boundary layer is temporarily unavailable.')
    return fmap

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Best Crop by Governorate', 'Best Locations in Egypt', 'Interactive Product Map', 'Matplotlib Ranking', 'Stacked Bar Analysis'])
with tab1:
    a, b = st.columns(2)
    governorate = a.selectbox('Governorate', sorted(records['governorate'].unique()))
    category = b.selectbox('Product Category', ['All'] + sorted(records['product_category'].unique()))
    data = valid(records[records['governorate'].eq(governorate)])
    if category != 'All':
        data = data[data['product_category'].eq(category)]
    for column in ['area_feddan', 'production_ton', 'yield_ton_per_feddan']:
        maximum = data[column].max()
        data[f'{column}_score'] = data[column] / maximum if pd.notna(maximum) and maximum > 0 else 0
    data['performance_score'] = 100 * (0.50 * data['yield_ton_per_feddan_score'] + 0.30 * data['production_ton_score'] + 0.20 * data['area_feddan_score'])
    data = data.sort_values('performance_score', ascending=False)
    if len(data):
        top = data.iloc[0]
        st.success(f"Leading product in the selected records: {top['product']} — performance score {top['performance_score']:.0f}/100")
        x, y, z = st.columns(3)
        x.metric('Cultivated area', f"{top['area_feddan']:,.0f} feddan")
        y.metric('Production', f"{top['production_ton']:,.0f} tons" if pd.notna(top['production_ton']) else '—')
        z.metric('Yield', f"{top['yield_ton_per_feddan']:.2f} t/feddan" if pd.notna(top['yield_ton_per_feddan']) else '—')
        figure = px.bar(data.head(10).sort_values('performance_score'), x='performance_score', y='product', orientation='h', color='product_category', text='performance_score', color_discrete_sequence=px.colors.qualitative.Set2)
        figure.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        figure.update_layout(height=480, plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=0, r=30, t=20, b=0))
        st.plotly_chart(figure, use_container_width=True)

with tab2:
    product = st.selectbox('Product', sorted(records['product'].unique()), key='national_crop')
    display_metric = st.radio('Rank Governorates By', ['Cultivated Area', 'Production', 'Yield'], horizontal=True)
    metric = metric_column(display_metric)
    summary = product_summary(records, product, metric)
    if len(summary):
        leader = summary.iloc[0]
        st.info(f"{leader['governorate']} ranks first for {product} by {display_metric.lower()} in the available data.")
        figure = px.bar(summary.head(15).sort_values(metric), x=metric, y='governorate', orientation='h', color=metric, color_continuous_scale='YlGn', labels={metric: display_metric, 'governorate': 'Governorate'})
        figure.update_layout(height=530, plot_bgcolor='white', paper_bgcolor='white', coloraxis_showscale=False)
        st.plotly_chart(figure, use_container_width=True)

with tab3:
    product = st.selectbox('Product to Display', sorted(records['product'].unique()), key='map_crop')
    display_metric = st.selectbox('Map Metric', ['Cultivated Area', 'Production', 'Yield'], key='map_metric')
    metric = metric_column(display_metric)
    summary = product_summary(records, product, metric)
    callout('The GeoJSON map colors governorates according to the selected crop metric. Select a product to view its main cultivation locations.')
    st_folium(build_map(summary, product, metric), height=570, use_container_width=True)

with tab4:
    a, b = st.columns(2)
    product = a.selectbox('Product', sorted(records['product'].unique()), key='matplotlib_product')
    display_metric = b.selectbox('Metric', ['Production', 'Cultivated Area', 'Yield'], key='matplotlib_metric')
    metric = metric_column(display_metric)
    summary = product_summary(records, product, metric).head(15).sort_values(metric)
    st.pyplot(governorate_ranking_chart(summary, display_metric, metric), use_container_width=True)

with tab5:
    display_metric = st.selectbox('Stacked Bar Metric', ['Cultivated Area', 'Production'], key='stacked_metric')
    metric = {'Cultivated Area': 'area_feddan', 'Production': 'production_ton'}[display_metric]
    st.plotly_chart(stacked_category_chart(valid(records), display_metric, metric), use_container_width=True)
