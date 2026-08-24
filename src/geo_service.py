import requests
import streamlit as st

GEOJSON_URL = 'https://services1.arcgis.com/dRxtwawTOPZm6CPj/ArcGIS/rest/services/egypt_governorates/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson'
NAME_MAPPING = {
    'Ash Sharqiyah': 'Al Sharqia', 'Al Iskandariyah': 'Alexandria', 'Al Buhayrah': 'Beheira',
    'Bani Suwayf': 'Beni Suef', 'Al Qahirah': 'Cairo', 'Ad Daqahliyah': 'Dakahlia',
    'Dumyat': 'Damietta', 'Al Fayyum': 'Faiyum', 'Al Gharbiyah': 'Gharbiyya',
    'Al Jizah': 'Giza', 'Al Isma`iliyah': 'Ismailia', 'Kafr ash Shaykh': 'Kafr el-Sheikh',
    'Al Uqsur': 'Luxor', 'Al Minya': 'Minya', 'Al Minufiyah': 'Monufia',
    'Al Wadi al Jadid': 'New Valley', "Shamal Sina'": 'North Sinai',
    "Bur Sa`id": 'Port Said', 'Al Qalyubiyah': 'Qalyubia', 'Qina': 'Qena',
    'Al Bahr al Ahmar': 'Red Sea', 'Suhaj': 'Sohag', "Janub Sina'": 'South Sinai',
    'As Suways': 'Suez'
}

@st.cache_data(ttl=86400 , show_spinner=False)
def load_governorate_geojson():
    response = requests.get(GEOJSON_URL, timeout=30)
    response.raise_for_status()
    geojson = response.json()
    for feature in geojson['features']:
        source_name = feature['properties'].get('NAME_1')
        feature['properties']['governorate'] = NAME_MAPPING.get(source_name, source_name)
    return geojson
