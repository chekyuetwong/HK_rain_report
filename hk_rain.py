import streamlit as st
import os, sys

@st.cache
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
opts = FirefoxOptions()
opts.add_argument("--headless")

import matplotlib.pyplot as plt
from datetime import datetime

Title = "Measured Tide Levels"
st.title(Title)

Initialisation = True
Download = True
Quarry_Bay = st.checkbox('Quarry Bay', value=True)
Tai_Po_Kau = st.checkbox('Tai Po Kau', value=True)
Tsim_Bei_Tsui = st.checkbox('Tsim Bei Tsui', value=True)
Tai_O = st.checkbox('Tai O', value=True)

from datetime import datetime
year = datetime.now().year
month = datetime.now().month

import pandas as pd
from bs4 import BeautifulSoup
import time

import matplotlib.dates as mdates

@st.cache
def hko_table_csv(url):
    driver = webdriver.Firefox(options=opts)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    mainc = soup.find(id='mainContent')
    rows = mainc.find_all('tr')
    data=[]
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values

    driver.close() # closing the webdriver
    return data

@st.cache
def tide_data(station):
  station=str(station)
  try: 
    URL="https://www.hko.gov.hk/en/tide/marine/realtide.htm?s="+station+"&t=TABLE"
    print("Updated data retrieved from: ", URL)
    data = hko_table_csv(URL)
    df = pd.DataFrame(data)
    df1 = df.iloc[8:, 0:3]

    df1.columns=["Date", "Measured", "Predicted"]
    df1=df1.set_index("Date")
    df1.index = pd.to_datetime(df1.index)
    #df1.to_csv(fp("test_for_today"))

    df1["Measured"] = pd.to_numeric(df1["Measured"], errors='coerce')
    df1["Predicted"]=pd.to_numeric(df1["Predicted"], errors='coerce')
    #print(df1)
    return df1

  except:
    print("Error encountered. The plot for "+station+" was unsuccessful.")


fig = plt.figure(figsize=[15,5])
ax = fig.add_subplot(1,1,1)

if Quarry_Bay:
  QUB=tide_data("QUB")
  plt.plot(QUB.index, QUB["Measured"], label="Quarry Bay")

if Tai_Po_Kau:
  TPK=tide_data("TPK")
  plt.plot(TPK.index, TPK["Measured"], label="Tai Po Kau")

if Tsim_Bei_Tsui:
  TBT=tide_data("TBT")
  plt.plot(TBT.index, TBT["Measured"], label="Tsim Bei Tsui")
if Tai_O:
  TAO=tide_data("TAO")
  plt.plot(TAO.index, TAO["Measured"], label="Tai O")

hours = mdates.HourLocator(interval = 3)
h_fmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
ax.set_title(Title, size=20)
ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(h_fmt)
ax.grid()
ax.set_ylabel("Tide Level (mCD)")

fig.autofmt_xdate()

plt.legend()
timestamp=max(QUB.index).strftime("%Y-%m-%d_%H-%M")
filename = Title+".png"
#plt.savefig(filename, bbox_inches='tight')
#plt.show()
st.pyplot(fig)
