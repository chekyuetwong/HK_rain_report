import streamlit as st
import os, sys
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
opts = FirefoxOptions()
opts.add_argument("--headless")
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
import time
import matplotlib.dates as mdates
import requests
from st_aggrid import AgGrid
st.set_page_config(layout="wide")


def API():
  Initialisation = True
  Download = True
  with st.sidebar:
    st.title("HKO Data")
    url_spec=st.checkbox("Specific URL")
    if url_spec:
        type=st.selectbox("Type:", ("CSV", "JSON"))
        url = st.text_input("url input", "")
        #https://api.data.gov.hk/v1/historical-archive/get-file?url=https%3A%2F%2Fdata.weather.gov.hk%2FweatherAPI%2Fhko_data%2Ftide%2FALL_en.csv&time=20220613-0000
        #https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=en

    else:
        type="JSON"
        dataset=st.selectbox("Dataset", ("HHOT", "HLT", "SRS", "MRS", "LHL", "LTMV", "CLMTEMP", "RYES"))
        station=st.selectbox("Station", ("QUB", "TPK", "HKO"))
        year = st.text_input("Year", "2022")
        month = st.text_input("Month", "")
        day = st.text_input("Day", "")
        url= "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?lang=en&rformat=json&dataType="+dataset+"&station="+station+"&year="+year+"&month="+month+"&day="+day
  
  if type == "CSV":
      df = pd.read_csv(url)
      AgGrid(df, height=800,fit_columns_on_grid_load=True)
  elif url_spec:
      req=requests.get(url)
      st.write(req.json())
  else:
      req=requests.get(url)
      df = pd.DataFrame(req.json()['data'] , columns=req.json()['fields'] )
      AgGrid(df, height=800,fit_columns_on_grid_load=True)


API()