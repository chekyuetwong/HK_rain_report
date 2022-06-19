import streamlit as st
import os, sys
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
opts = FirefoxOptions()
opts.add_argument("--headless")
driver = webdriver.Firefox(options=opts)
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
import time
import matplotlib.dates as mdates

@st.experimental_singleton(suppress_st_warning=True)
def hko_table_csv(url):
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    mainc = soup.find(id='mainContent')
    rows = mainc.find_all('tr')
    data=[]
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values

    #driver.close() # closing the webdriver
    return data

@st.experimental_singleton(suppress_st_warning=True)
def tide_data(station):
  #station=str(station)
  try: 
  #if True:
    URL="https://www.hko.gov.hk/en/tide/marine/realtide.htm?s="+station+"&t=TABLE"
    #st.sidebar.success("Updated data to be retrieved from: "+URL)
    data = hko_table_csv(URL)
    df = pd.DataFrame(data)
    df1 = df.iloc[8:, 0:3]

    df1.columns=["Date", "Measured", "Predicted"]
    df1=df1.set_index("Date")
    df1.index = pd.to_datetime(df1.index)
    #df1.to_csv(fp("test_for_today"))

    df1["Measured"] = pd.to_numeric(df1["Measured"], errors='coerce')
    df1["Predicted"]=pd.to_numeric(df1["Predicted"], errors='coerce')
    st.sidebar.success("Data Retrieval for "+station+" was successful.")
    return df1

  except:
    st.sidebar.warning("Error encountered. Data Retrieval for "+station+" was unsuccessful.")



def tide():
  Title = "Measured Tide Levels"

  Initialisation = True
  Download = True
  with st.sidebar:
    st.title("Measured Tide Levels (Nearest 24 hours)")
    Title = st.text_input("Plot Title", "Measured Tide Levels")
    #Quarry_Bay = st.checkbox('Quarry Bay', value=True)
    #Tai_Po_Kau = st.checkbox('Tai Po Kau', value=True)
    #Tsim_Bei_Tsui = st.checkbox('Tsim Bei Tsui', value=True)
    #Tai_O = st.checkbox('Tai O', value=True)
    if st.button('Refresh Data from HKO'):
      tide_data.clear()
      hko_table_csv.clear()
  
  df1=tide_data("QUB")
  df1.columns="Quarry Bay "+df1.columns
  df2 = tide_data("TPK")
  df2.columns="Tai Po Kau "+df2.columns
  df3 = tide_data("TBT")
  df3.columns="Tsim Bei Tsui "+df3.columns
  df4 = tide_data("TAO")
  df4.columns="Tai O "+df4.columns
  #st.write(df)
  #st.write(df2)
  df=pd.concat([df1, df2, df3, df4], axis=1, join="outer")
  #st.write(df)
  #df.loc[:,"Tsim Bei Tsui (Measured)", "Tsim Bei Tsui (Actual)"]=tide_data("TBT")
  #df.loc[:,"Tai O (Measured)", "Tai O (Actual)"]=tide_data("TAO")
  #QUB=tide_data("QUB")
  #TPK=tide_data("TPK")
  #TBT=tide_data("TBT")
  #TAO=tide_data("TAO")



  #fig = plt.figure(figsize=[15,5])
  #ax = fig.add_subplot(1,1,1)

  #if Quarry_Bay:
  #  QUB=tide_data("QUB")
  #  plt.plot(QUB.index, QUB["Measured"], label="Quarry Bay")

  #if Tai_Po_Kau:
  #  TPK=tide_data("TPK")
  #  plt.plot(TPK.index, TPK["Measured"], label="Tai Po Kau")

  #if Tsim_Bei_Tsui:
  #  TBT=tide_data("TBT")
  #  plt.plot(TBT.index, TBT["Measured"], label="Tsim Bei Tsui")
  #if Tai_O:
  #  TAO=tide_data("TAO")
  #  plt.plot(TAO.index, TAO["Measured"], label="Tai O")

  #hours = mdates.HourLocator(interval = 3)
  #h_fmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
  #ax.set_title(Title, size=20)
  #ax.xaxis.set_major_locator(hours)
  #ax.xaxis.set_major_formatter(h_fmt)
  #ax.grid()
  #ax.set_ylabel("Tide Level (mCD)")
  #fig.autofmt_xdate()
  #plt.legend()
  #timestamp=max(QUB.index).strftime("%Y-%m-%d_%H-%M")
  #filename = Title+".png"
  #plt.savefig(filename, bbox_inches='tight')
  #plt.show()
  fig = px.line(df)
  fig.update_layout(autotypenumbers='convert types', width=1200, height=600)
  st.plotly_chart(fig)
  #st.write(df)
  st.write("Data Source: https://www.hko.gov.hk/en/tide/marine/realtide.htm")
