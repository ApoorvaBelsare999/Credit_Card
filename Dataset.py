# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 11:54:54 2022

@author: user
"""

import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")


st.markdown("# DataFrame Demo")
data = pd.read_csv(r"C:\Users\user\Downloads\default of credit card clients.csv")
st.write(data)