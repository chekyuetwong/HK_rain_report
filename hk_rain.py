import streamlit as st
from tide import tide

def home_page():
  st.markdown("""# Welcome to this App
  This is a web app under alpha testing regarding Hong Kong weather.
  """)

to_func = {
  "Home": home_page,
  "Tide": tide
}

demo_name = st.sidebar.selectbox("Page Select", to_func.keys())
to_func[demo_name]()