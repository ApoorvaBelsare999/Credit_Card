import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")


st.markdown("# DataFrame Demo")
data = pd.read_csv('default of credit card clients.csv')
st.write(data)
