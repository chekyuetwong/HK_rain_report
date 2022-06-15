from tide import tide
from warning import warning
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

@st.cache
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')



def home_page():
  st.markdown("""# Welcome to this App
  This is a web app under alpha testing regarding Hong Kong weather.
  """)

to_func = {
  "Home": home_page,
  "Tide": tide,
  "Warning Timeline":warning
}


st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 600px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 600px;
        margin-left: -600px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

_ = installff()
demo_name = st.sidebar.selectbox("Page Select", to_func.keys())
to_func[demo_name]()