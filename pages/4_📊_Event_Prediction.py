import streamlit as st
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import datetime

st.set_page_config(layout = "wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Future Event Predictions</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Predict weekly booking for your future events using our trained AI model</h5>", unsafe_allow_html=True)

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
    dfs['StartDate'] = dfs.StartDate.dt.date
    return dfs

def booking_features(dfs):
    dfs = dfs.copy()
    dfs = addSeason(dfs)
    dfs['bookingWeeksToEvent'] = round(abs((dfs['StartDate'] - dfs['StatusCreatedDate']).dt.days)/7,0)
    dfs['bookingquarter'] = dfs.StatusCreatedDate.dt.quarter
    dfs['bookingweekofyear'] = np.uint32(np.int32(dfs.StatusCreatedDate.dt.isocalendar().week))
    dfs['bookingmonth'] = dfs.StatusCreatedDate.dt.month
    dfs['bookingyear'] = dfs.StatusCreatedDate.dt.year
    return dfs


def predictWeeksToSell(df):
    xbg_weeks = XGBRegressor()
    xbg_weeks.load_model("XGBoostTotalweeks.json")
    df2 = event_features(Company).drop(labels=['StartDate', 'EventSeason'], axis=1)
    weekPred = xbg_weeks.predict(df2)
    # st.table(event_features(df))
    return round(weekPred[0])


def generateWeeksData(eventDate, period):
    freq = '-1W-SUN'
    times = pd.date_range(eventDate, periods=period, freq=freq)
    times = pd.DataFrame(reversed(times))
    times['StartDate'] = eventDate
    times.columns = ['StatusCreatedDate', 'StartDate']
    times=booking_features(times)
    return times

def predictWeekyBookings(df):
    xbg_weekly = XGBRegressor()
    xbg_weekly.load_model("XGBoostweeklybooking.json")
    df2 = df.drop(labels=['StatusCreatedDate', 'EventSeason',  'StartDate' ], axis=1)
    weeklyPred = xbg_weekly.predict(df2)
    weekly_pred_df = pd.DataFrame()
    weekly_pred_df['Booking Week'] = df['StatusCreatedDate'].dt.date

    predictions =[]
    weekNumber = []
    index = len(weeklyPred) +1
    for row in weeklyPred:
        if row < 0 : 
            predictions.append(abs(round(row))) 
        else: 
            predictions.append(abs(round(row)))
        index = index-1
        weekNumber.append(index)
        # index-1

    weekly_pred_df['Weeks to event'] =weekNumber
    weekly_pred_df['Booking Predictions'] = predictions

    return weekly_pred_df


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

        weeks_df = pd.DataFrame(generateWeeksData(pd.to_datetime(d, errors='coerce'), predictedWeeks))
        weeks_df_predict = predictWeekyBookings(weeks_df)
        st.info("Weekly booking predictions") 
        st.dataframe(weeks_df_predict, use_container_width=True)
        st.info("A graph showing the weekly booing predictions") 
        st.line_chart(weeks_df_predict, x='Booking Week', y='Booking Predictions')


