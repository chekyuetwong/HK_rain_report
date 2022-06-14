import streamlit as st
import os, sys
import pandas as pd
import matplotlib.pyplot as plt


def tide():
  Title = "Measured Tide Levels"
  st.title(Title)

  Initialisation = True
  Download = True
  Quarry_Bay = st.checkbox('Quarry Bay', value=True)
  Tai_Po_Kau = st.checkbox('Tai Po Kau', value=True)
  Tsim_Bei_Tsui = st.checkbox('Tsim Bei Tsui', value=True)
  Tai_O = st.checkbox('Tai O', value=True)

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
  #timestamp=max(QUB.index).strftime("%Y-%m-%d_%H-%M")
  filename = Title+".png"
  #plt.savefig(filename, bbox_inches='tight')
  #plt.show()
  st.pyplot(fig)
