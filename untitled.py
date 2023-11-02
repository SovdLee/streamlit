import pandas as pd
import numpy as np
import datetime
import joblib
from keras.models import load_model
from haversine import haversine
from urllib.parse import quote
import streamlit as st
from streamlit_folium import st_folium
import folium
import branca
from geopy.geocoders import Nominatim
import ssl
from urllib.request import urlopen
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="",
    page_icon=":bi bi-heart-pulse-fill:"
)