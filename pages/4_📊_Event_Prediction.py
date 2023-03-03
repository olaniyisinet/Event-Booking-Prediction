import streamlit as st
import pandas as pd
import numpy as np


!pip install xgboost

import xgboost as xgb

st.set_page_config(layout = "wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Future Event Predictions</h1>", unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align: center;'>Collaborative App Development Coursework</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Predict the booking for your future events using our trained AI model</h5>", unsafe_allow_html=True)
  

# ticketsmodel = load_model()