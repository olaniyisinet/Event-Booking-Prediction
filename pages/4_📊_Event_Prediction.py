import streamlit as st
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import datetime

st.set_page_config(layout = "wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Future Event Predictions</h1>", unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align: center;'>Collaborative App Development Coursework</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Predict the booking for your future events using our trained AI model</h5>", unsafe_allow_html=True)


# To create Season and season code column
def addSeason(df):
    _condition_winter = (df.StartDate.dt.month>=1)&(df.StartDate.dt.month<=3)
    _condtion_spring = (df.StartDate.dt.month>=4)&(df.StartDate.dt.month<=6)
    _condition_summer = (df.StartDate.dt.month>=7)&(df.StartDate.dt.month<=9)
    _condition_autumn = (df.StartDate.dt.month>=10)&(df.StartDate.dt.month<=12)

    df['EventSeason'] = np.where(_condition_winter,'Winter',np.where(_condtion_spring,'Spring',np.where(_condition_summer,'Summer',np.where(_condition_autumn,'Autumn',np.nan))))
    eventSeasonCode = []
    for row in df['EventSeason']:
        if row == 'Autumn': eventSeasonCode.append(0)
        if row == 'Spring': eventSeasonCode.append(1)
        if row == 'Summer': eventSeasonCode.append(2)
        if row == 'Winter': eventSeasonCode.append(3)
    df['SeasonCode'] = eventSeasonCode
    return df

def event_features(dfs):
    dfs = dfs.copy()
    dfs = addSeason(dfs)
    dfs['eventdayofweek'] = dfs.StartDate.dt.dayofweek
    dfs['eventquarter'] = dfs.StartDate.dt.quarter
    dfs['eventmonth'] = dfs.StartDate.dt.month
    dfs['eventyear'] = dfs.StartDate.dt.year
    dfs['eventdayofyear'] = dfs.StartDate.dt.dayofyear
    dfs['eventdayofmonth'] = dfs.StartDate.dt.day
    dfs['eventweekofyear'] = np.uint32(np.int32(dfs.StartDate.dt.isocalendar().week))
    return dfs

def booking_features(dfs):
    dfs = dfs.copy()
    dfs['bookingdayofweek'] = dfs.StatusCreatedDate.dt.dayofweek
    dfs['bookingquarter'] = dfs.StatusCreatedDate.dt.quarter
    dfs['bookingmonth'] = dfs.StatusCreatedDate.dt.month
    dfs['bookingyear'] = dfs.StatusCreatedDate.dt.year
    dfs['bookingdayofyear'] = dfs.StatusCreatedDate.dt.dayofyear
    dfs['bookingdayofmonth'] = dfs.StatusCreatedDate.dt.day
    dfs['bookingweekofyear'] = dfs.StatusCreatedDate.dt.isocalendar().week
    return dfs


def predictWeeksToSell(df):
    xbg_weeks = XGBRegressor()
    # data =[{"SeasonCode":2,"eventdayofweek":3,"eventquarter":3,"eventmonth":7,"eventyear":2022,"eventdayofyear":209,"eventdayofmonth":28,"eventweekofyear":30}]
    xbg_weeks.load_model("XGBoostTotalweeks.json")
    # df = pd.DataFrame.from_dict(data)
    df2 = event_features(Company).drop(labels=['StartDate', 'EventSeason'], axis=1)
    weekPred = xbg_weeks.predict(df2)
    st.table(event_features(df))
    return round(weekPred[0])
    # print(round(predings[0]))
    # st.write("Your event will be booked for ", round(weekPred[0]), "weeks")

# print(predictWeeksToSell())


with st.container():
    #Input for users to select their event date
    d = st.date_input(
        "When\'s your event happening? Please select the date",
        datetime.date(2023, 4, 1))
    st.write('Your event is happening on:', d)
    
    if st.button('Click to get booking predictions'):
        #Generating data frame
        Company = pd.DataFrame.from_dict([{"StartDate": d}])
        Company['StartDate'] = pd.to_datetime(d, errors='coerce')
        predictedWeeks = predictWeeksToSell(Company)

        st.write("Your event is likely to be booked for ", predictedWeeks, "weeks")

