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
from datetime import datetime


import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
opts = FirefoxOptions()
opts.add_argument("--headless")
from datetime import time as tm

@st.cache
def grab_signal(url, c_name, from_row=4):
  driver = webdriver.Firefox(options=opts)
  driver.get(url)
  time.sleep(1)
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  mainc = soup.find(id='mainContent')
  rows = mainc.find_all('tr')
  out=[]
  for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      out.append([ele for ele in cols if ele])

  out_df=pd.DataFrame(out[from_row:], columns=c_name)
  driver.close()
  out_df.loc[:,"End"]=pd.to_datetime(out_df.loc[:,"edate"])+pd.to_timedelta(out_df.loc[:, "etime"]+":00")
  out_df.loc[:,"Start"]=pd.to_datetime(out_df.loc[:,"sdate"])+pd.to_timedelta(out_df.loc[:, "stime"]+":00") 
  out_df.loc[:, "Continued"] = False
  out_df.loc[:, "Superseded"] = False

  def convert_min(in_series):
    return in_series.total_seconds()/60

  out_df.loc[:, "Issuance Interval(min)"] = (out_df.Start - out_df.Start.shift(1)).apply(convert_min)
  out_df.loc[out_df.End.shift(1)==out_df.Start, "Continued"] = True
  out_df.loc[out_df.End==out_df.Start.shift(-1), "Superseded"] = True

  return out_df

def pos_map(pos):
  if pos in [1,2,3,4,5]:
    pos=(pos)*2
  else:
    pos=-999
  return pos

def plot_bar(in_df, ss, ee, colour, pos, sname="", label=False):

  plot_df = in_df.copy()

  plot_df=plot_df.loc[(plot_df.loc[:, "End"]>=ss)&(plot_df.loc[:,"Start"]<=ee), :]

  if plot_df.shape[0]==0:
    return
  
  if plot_df.iloc[0, :].loc["Start"]<ss:
    print("Alert: \n{} Signal started at {}. \nAdjust the time to show the entire alert.\n".format(sname, plot_df.iloc[0, :].loc["Start"]))
    tag=datetime.strftime(plot_df.iloc[0, :].loc["Start"], "%H:%M")+"\n⟱"
    plt.annotate(tag, xy=(pos, ss), textcoords='data', fontsize=8, ha='center')
  if plot_df.iloc[-1, :].loc["End"]>ee:
    print("Alert: \n{} Signal ended at {}. \nAdjust the time to show the entire alert.\n".format(sname, plot_df.iloc[-1, :].loc["End"]))
    tag="⟱\n"+datetime.strftime(plot_df.iloc[-1, :].loc["End"], "%H:%M")
    plt.annotate(tag, xy=(pos, ss+0.95*(ee-ss)), textcoords='data', fontsize=8, ha='center', color='white')
  plot_df = plot_df.set_index("Start")

  begin = plot_df.index
  plot2=plot_df.set_index("End")
  end = plot2.index
  #print(begin)
  #print(end)

  plt.bar(pos,  end-begin, bottom=begin, color=colour, width=0.5)
  
  x=[]
  x.extend([pos-0.6 for i in range(len(begin))])
  t=["%02d:%02d" % t for t in zip(begin.hour.tolist(), begin.minute.tolist())]
  i=0
  for xy in zip(x, begin): 
    plt.annotate(t[i], xy=xy, textcoords='data', fontsize=10, ha='center')
    i+=1
  j=0
  if label==True:
    x2=[]
    x2.extend([pos+0.4 for i in range(len(begin))])
    t="T"+plot_df.loc[:,"signal"]
    j=0
    for xy in zip(x2, begin): # + timedelta(minutes=90)): 
      plt.annotate(t[j], xy=xy, textcoords='data', fontsize=10, color='k', ha='center')
      j+=1
  
  
  plot_df = plot_df.loc[plot_df.loc[:, "Superseded"]==False]
  #print(plot_df)
  begin = plot_df.index
  plot2=plot_df.set_index("End")
  end = plot2.index

  x1=[]
  x1.extend([pos+0.3 for i in range(len(end))])  
  t1=["%02d:%02d" % t for t in zip(end.hour.tolist(), end.minute.tolist())]
  j=0
  for xy in zip(x1, end): 
    plt.annotate(t1[j], xy=xy, textcoords='data', fontsize=10)
    j+=1
  plt.annotate(sname, xy=(pos, ee), textcoords='data', fontsize=10, ha='center', bbox=dict(fc="white"))

def warning():

  default_time1 = tm(0,0)
  default_time2 = tm(23,59)
  

  with st.sidebar:
    st.markdown("---")
    st.title("Weather Warning Signal Timeline")
    st.markdown("---")
    Title = st.text_input("Timeline Title", "Event Timeline")
  
    a1, a2, a3 = st.columns(3)
    with a1:
      Start_Date = st.date_input("Start Date")
      Start_Time = st.time_input('Start Time', default_time1)
    with a2:
      End_Date = st.date_input("End Date")
      End_Time = st.time_input('End Time',  default_time2)

    b1, b2, b3, b4, b5 = st.columns(5)
    with b1:
      Rainstorm = st.selectbox("Rainstorm", (0,1,2,3,4,5), 1)
    with b2:
      SAFNNT = st.selectbox("SAFNNT", (0,1,2,3,4,5), 2)
    with b3:
      Tropical_Cyclone = st.selectbox("Tropical Cyclone", (0,1,2,3,4,5), 3)
    with b4:
      Landslip = st.selectbox("Landslip", (0,1,2,3,4,5), 4)
    with b5:
      Thunderstorm = st.selectbox("Thunderstorm", (0,1,2,3,4,5), 5)
    Image_Height = st.slider('Image Height', 5, 30, 10)
    st.write("""#Timeline Customisation
    """)

  ds=datetime.combine(Start_Date,Start_Time)
  de=datetime.combine(End_Date,End_Time)
  #st.write(ds)
  #st.write(de)

  Rainstorm = pos_map(Rainstorm)
  SAFNNT = pos_map(SAFNNT)
  Thunderstorm = pos_map(Thunderstorm)
  Landslip = pos_map(Landslip)
  Tropical_Cyclone = pos_map(Tropical_Cyclone)
  
  year = datetime.now().year
  month = datetime.now().month

  rainstorm_url = "https://www.hko.gov.hk/en/wxinfo/climat/warndb/warndb3.shtml?opt=3&rcolor=All+colours&start_ym=199803&end_ym=%04d%02d&submit=Submit+Query"%(year, month)
  safnnt_url = "https://www.hko.gov.hk/en/wxinfo/climat/warndb/warndb11.shtml?opt=11&start_ym=199803&end_ym=%04d%02d&submit=Submit+Query"%(year, month)
  landslip_url = "https://www.hko.gov.hk/en/wxinfo/climat/warndb/warndb4.shtml?opt=4&start_ym=199801&end_ym=%04d%02d&submit=Submit+Query"%(year, month)
  tc_url = "https://www.hko.gov.hk/en/wxinfo/climat/warndb/warndb1.shtml?opt=1&sgnl=1.or.higher&start_ym=199803&end_ym=%04d%02d&submit=Submit+Query"%(year, month)
  thunderstorm_url = "https://www.hko.gov.hk/en/wxinfo/climat/warndb/warndb5.shtml?opt=5&start_ym=199801&end_ym=%04d%02d&submit=Submit+Query"%(year, month)

  rainstorm_col = ['signal', 'stime', 'sdate', 'etime','edate', 'duration']
  safnnt_col = ['stime', 'sdate', 'etime','edate', 'duration']
  landslip_col = safnnt_col
  tc_col = ['intensity','name','signal', 'stime', 'sdate', 'etime','edate', 'duration']
  thunderstorm_col = safnnt_col

  rainstorm_df = grab_signal(rainstorm_url, rainstorm_col)
  tc_df = grab_signal(tc_url, tc_col, 5)
  safnnt_df = grab_signal(safnnt_url, safnnt_col)
  landslip_df = grab_signal(landslip_url, landslip_col)
  thunderstorm_df = grab_signal(thunderstorm_url, thunderstorm_col)

  warning_string=""
  
  Image_Width = max(Rainstorm, SAFNNT, Thunderstorm, Landslip, Tropical_Cyclone)+2

  fig, ax = plt.subplots(figsize=(Image_Width,Image_Height), dpi=100)
  plt.title(Title+"\n", fontsize=30)

  if Rainstorm != -999:
    plot_bar(rainstorm_df.loc[rainstorm_df.loc[:,"signal"]=="Amber"], ds, de, 'yellow', Rainstorm, "Rainstorm")
    plot_bar(rainstorm_df.loc[rainstorm_df.loc[:,"signal"]=="Red"], ds, de, 'r', Rainstorm, "Rainstorm")
    plot_bar(rainstorm_df.loc[rainstorm_df.loc[:,"signal"]=="Black"], ds, de, 'k', Rainstorm, "Rainstorm")

  if SAFNNT != -999:
    plot_bar(safnnt_df, ds, de, 'g', SAFNNT, "SAFNNT")

  if Thunderstorm != -999:
    plot_bar(thunderstorm_df, ds, de, 'black', Thunderstorm, "Thunderstorm")

  if Landslip != -999:
    plot_bar(landslip_df, ds, de, 'orange', Landslip, "Landslip")

  if Tropical_Cyclone != -999:
    tc_dfa=tc_df.copy()
    tc_dfa.loc[:, "T"]=tc_df.signal.str.extract('(^\d*)')
    plot_bar(tc_dfa.loc[tc_dfa.loc[:,"T"]=="1"], ds, de, '#0000CC', Tropical_Cyclone, "Tropical \nCyclone", True)
    plot_bar(tc_dfa.loc[tc_dfa.loc[:,"T"]=="3"], ds, de, '#0000AA', Tropical_Cyclone, "Tropical \nCyclone", label=True)
    plot_bar(tc_dfa.loc[tc_dfa.loc[:,"T"]=="8"], ds, de, '#000088', Tropical_Cyclone, "Tropical \nCyclone", label=True)
    plot_bar(tc_dfa.loc[tc_dfa.loc[:,"T"]=="9"], ds, de, '#000044', Tropical_Cyclone, "Tropical \nCyclone", label=True)
    plot_bar(tc_dfa.loc[tc_dfa.loc[:,"T"]=="10"], ds, de, '#000022', Tropical_Cyclone, "Tropical \nCyclone", label=True)


  myFmt = mdates.DateFormatter('%Y/%m/%d\n%H:%M')
  ax.yaxis.set_major_formatter(myFmt)
  plt.grid(b=None)
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['bottom'].set_visible(False)
  ax.spines['left'].set_visible(False)
  plt.xticks([])
  ax.grid(axis='x')
  plt.annotate('', xy=(-2, ds), xytext=(-2, de), arrowprops=dict(arrowstyle='<|-,head_length=5,head_width=0.5', color='black', lw=5))
  ax.set_ylim(de, ds)
  ax.set_xlim(0, Image_Width+2)
  ax.margins(0.1,0.1)
  ax.autoscale(enable=None, axis="x", tight=True)

  st.pyplot(fig)
