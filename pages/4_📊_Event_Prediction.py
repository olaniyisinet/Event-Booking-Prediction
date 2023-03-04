import streamlit as st
import pandas as pd
import numpy as np
from xgboost import XGBRegressor

st.set_page_config(layout = "wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Future Event Predictions</h1>", unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align: center;'>Collaborative App Development Coursework</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Predict the booking for your future events using our trained AI model</h5>", unsafe_allow_html=True)
  


# xbg_reg = XGBRegressor()
# # xbg_reg.load_model("XGBoostTotalTickets.json")

# # X_test = [{"index":1703,"SeasonCode":2,"LastbookingWeek":1,"FirstbookingWeek":22,"TotalWeeksToSell":21,"eventdayofweek":3,"eventquarter":3,"eventmonth":7,"eventyear":2022,"eventdayofyear":209,"eventdayofmonth":28,"eventweekofyear":30}]
# # data = pd.DataFrame.from_dict(X_test)
# # predings = xbg_reg.predict(data)
# # st.table(predings)


def predictWeeksToSell():
    xbg_weeks = XGBRegressor()
    data =[{"SeasonCode":2,"TotalTickets":20,"LastbookingWeek":1.0,"FirstbookingWeek":22.0,"eventdayofweek":3,"eventquarter":3,"eventmonth":7,"eventyear":2022,"eventdayofyear":209,"eventdayofmonth":28,"eventweekofyear":30}]
    xbg_weeks.load_model("XGBoostTotalweeks.json")
    df = pd.DataFrame.from_dict(data)
    predings = xbg_weeks.predict(df)
    st.table(predings)


predictWeeksToSell()