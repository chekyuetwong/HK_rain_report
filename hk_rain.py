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
from streamlit import caching
st.set_page_config(layout="wide")


def home_page():
  st.markdown("""# HK Weather Summary Web App
  ---
  Relevant Link:

  HK Daily Weather Insight: https://share.streamlit.io/chekyuetwong/hko_daily_insight/main/daily_insight.py

  """)

@st.cache
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

try:
  setup = False
  if setup == True:
    _ = installff()
    st.title("Web Driver Reset Completed")
    if st.button('Press to Restart'):
      setup=False
  else:
    from tide import tide
    from tide2 import tide2
    from warning import warning
    to_func = {
      "Home": home_page,
      "Tide (Nearest 24 Hours)": tide,
      "Tide (Since Jul 2020)": tide2,
      "Warning Timeline":warning
    }

  st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 500px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 500px;
            margin-left: -500px;
        }
        </style>
        """,unsafe_allow_html=True,)

  _ = installff()
  with st.sidebar:
    demo_name = st.selectbox("Applications", to_func.keys())
  to_func[demo_name]()

except:
  st.title("Error Encountered")
  st.write("Setup = "+str(setup))
  if st.button('Try Resolving by resetting the Web Driver'):
    setup = True