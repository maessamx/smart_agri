import math
import folium
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium
from src.geo_service import load_governorate_geojson
from src.data_service import load_records, product_summary
from src.ui.component import initialize_page, hero

st.set_page_config(page_title='Analytics Studio | Smart Agri Egypt', page_icon='📊', layout='wide', initial_sidebar_state='expanded')
initialize_page()
records = load_records()
hero('Analytics Studio', 'Explore crop ranking, governorate composition, and product distribution through Matplotlib, Plotly, and Folium.')

def valid(data):
    return data.dropna(subset=['area_feddan', 'production_ton'], how='all').copy()

def points_map(summary, product, metric):
    fmap = folium.Map(location=[27.2, 30.8], zoom_start=5, tiles='CartoDB positron')
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
        folium.GeoJsonTooltip(fields=['governorate'], aliases=['Governorate:'], sticky=False).add_to(folium.GeoJson(geojson).add_to(fmap))
    except Exception:
        st.warning('The governorate boundary layer is temporarily unavailable.')
    return fmap

tab1, tab2, tab3 = st.tabs(['Matplotlib Ranking', 'Stacked Bar by Governorate', 'Folium Distribution Map'])
with tab1:
    a, b = st.columns(2)
    product = a.selectbox('Product', sorted(records['product'].unique()))
    display_metric = b.selectbox('Metric', ['Production', 'Cultivated Area', 'Yield'])
    metric = {'Production': 'production_ton', 'Cultivated Area': 'area_feddan', 'Yield': 'yield_ton_per_feddan'}[display_metric]
    summary = product_summary(records, product, metric).head(15).sort_values(metric)
    figure, axis = plt.subplots(figsize=(10, 6))
    axis.barh(summary['governorate'], summary[metric], color='#27734D')
    axis.set_xlabel(display_metric)
    axis.set_ylabel('Governorate')
    axis.grid(axis='x', alpha=.18)
    axis.spines[['top', 'right']].set_visible(False)
    figure.tight_layout()
    st.pyplot(figure, use_container_width=True)

with tab2:
    display_metric = st.selectbox('Stacked Bar Metric', ['Cultivated Area', 'Production'])
    metric = {'Cultivated Area': 'area_feddan', 'Production': 'production_ton'}[display_metric]
    grouped = valid(records).groupby(['governorate', 'product_category'], as_index=False)[metric].sum()
    figure = px.bar(grouped, x='governorate', y=metric, color='product_category', barmode='stack', color_discrete_sequence=px.colors.qualitative.Set2, labels={'governorate': 'Governorate', 'product_category': 'Product Category', metric: display_metric})
    figure.update_layout(height=580, plot_bgcolor='white', paper_bgcolor='white', xaxis_tickangle=-45)
    st.plotly_chart(figure, use_container_width=True)

with tab3:
    product = st.selectbox('Product', sorted(records['product'].unique()), key='distribution_product')
    display_metric = st.selectbox('Map Metric', ['Cultivated Area', 'Production', 'Yield'], key='distribution_metric')
    metric = {'Cultivated Area': 'area_feddan', 'Production': 'production_ton', 'Yield': 'yield_ton_per_feddan'}[display_metric]
    summary = product_summary(records, product, metric)
    st_folium(points_map(summary, product, metric), height=570, use_container_width=True)
