# This is the page is where the event prediction happens. 
# According to the client, the client wants to be able to tell their customers how long it will take for people to book their event, possible weekly bookings, and the percentage cumulative bookings so far. 
# This will enable them to make necessary and informed decision on whether to increase or reduce the size of the event venue as the date of the event approaches. On this page, the client enters the event date, and clicks on the “Click to get booking predictions” button, the system evaluates and displays out weekly booking predictions in table and chart, with a little summary at the end.

import streamlit as st
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import datetime
import time

#Setting page layout
st.set_page_config(layout="wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Client Preferred Booking Predictions</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Predict weekly bookings for your future events using our trained AI model and select your prefered booking period</h5>", unsafe_allow_html=True)


# To create Season and season code column
def addSeason(df):
    _condition_winter = (df.StartDate.dt.month >= 1) & (df.StartDate.dt.month <= 3)
    _condtion_spring = (df.StartDate.dt.month >= 4) & (df.StartDate.dt.month <= 6)
    _condition_summer = (df.StartDate.dt.month >= 7) & (df.StartDate.dt.month <= 9)
    _condition_autumn = (df.StartDate.dt.month >= 10) & (df.StartDate.dt.month <= 12)

    df['EventSeason'] = np.where(_condition_winter, 'Winter', np.where(_condtion_spring, 'Spring', np.where(_condition_summer, 'Summer', np.where(_condition_autumn, 'Autumn', np.nan))))

    eventSeasonCode = []
    for row in df['EventSeason']:
        if row == 'Autumn': eventSeasonCode.append(0)
        if row == 'Spring': eventSeasonCode.append(1)
        if row == 'Summer': eventSeasonCode.append(2)
        if row == 'Winter': eventSeasonCode.append(3)

    df['SeasonCode'] = eventSeasonCode
    return df


#Extracting days, month, and weeks from event date
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
    dfs['bookingWeeksToEvent'] = round(abs((dfs['StartDate'] - dfs['StatusCreatedDate']).dt.days)/7, 0)
    dfs['bookingquarter'] = dfs.StatusCreatedDate.dt.quarter
    dfs['bookingweekofyear'] = np.uint32(np.int32(dfs.StatusCreatedDate.dt.isocalendar().week))
    dfs['bookingmonth'] = dfs.StatusCreatedDate.dt.month
    dfs['bookingyear'] = dfs.StatusCreatedDate.dt.year
    return dfs


def generateWeeksData(eventDate, period):
    freq = '-1W-SUN'
    times = pd.date_range(eventDate, periods=period, freq=freq)
    times = pd.DataFrame(reversed(times))
    times['StartDate'] = eventDate
    times.columns = ['StatusCreatedDate', 'StartDate']
    times = booking_features(times)
    return times


def predictWeekyBookings(df):
    xbg_weekly = XGBRegressor()
    xbg_weekly.load_model("XGBoostweeklybooking.json")
    df2 = df.drop(labels=['StatusCreatedDate', 'EventSeason',  'StartDate'], axis=1)
    weeklyPred = xbg_weekly.predict(df2)
    weekly_pred_df = pd.DataFrame()
    weekly_pred_df['Booking Weeks'] = df['StatusCreatedDate'].dt.date

    predictions = []
    weekNumber = []
    index = len(weeklyPred) + 1
    for row in weeklyPred:
        if row < 0:
            predictions.append(abs(round(row)))
        else:
            predictions.append(abs(round(row)))
        index = index-1
        weekNumber.append(index)

    weekly_pred_df['Weeks to event'] = weekNumber
    weekly_pred_df['Booking Predictions'] = predictions
    weekly_pred_df['Cumm. Total Prediction'] = pd.Series(
        predictions).cumsum()
    weekly_pred_df['Cumm. Booking %'] = round(
        (weekly_pred_df['Cumm. Total Prediction'] / weekly_pred_df['Booking Predictions'] .sum()) * 100, 0)

    return weekly_pred_df

def generateDays():
    days =[]
    for i in range(1, 31):
        days.append(i)
    days.reverse()
    return days

# def choosenPeriod(option):
#     weeks_df = pd.DataFrame(generateWeeksData(pd.to_datetime(d, errors='coerce'), option))
#     weeks_df_predict = predictWeekyBookings(weeks_df)

#     st.balloons()

#     totalBookings = weeks_df_predict['Booking Predictions'].sum()
#     st.success("Based on the selected booking period, total preditcted bookings for your event is: " + str(totalBookings), icon="ℹ️")

#     with st.container():
#         col1, col2 = st.columns(2)
#         col1.info("Weekly booking predictions")
#         col1.dataframe(weeks_df_predict, use_container_width=True)
#         col2.info("A plotting of the weekly booking predictions")
#         col2.line_chart(weeks_df_predict, x='Booking Weeks', y='Booking Predictions')

#     with st.container():
#         st.success("Summary")
#         season = weeks_df['EventSeason'][0:1].values

#         text = "From the predictions above, it shows that your event is happening in " + season + " " + str(pd.to_datetime(d, errors='coerce').year) + ", and it will take approximately "+str(predictedWeeks) + " weeks to get "+str(
#             totalBookings) + " bookings. The table above shows the weekly start date, weeks to event, predicted weekly bookings, the cummulative bookings, and the percentage bookings per week, while the line chart above shows the predicted weekly bookings against the weekly dates"

#         st.markdown(text[0])
#         st.markdown("In summary, if the cummulative booking is higher than your booking data after 70% of the booking period, you should perhaps start thinking of promotion or reducing the size of your venue depending on the observed differences.")
#         st.markdown("However, if the cummulative booking is lower than your booking data after 70% of the booking period, you should perhaps start thinking of increasing the size of your venue depending on the observed differences.")

with st.container():
    col1, col2 = st.columns(2)
    # Input for users to select their event date
    d = col1.date_input(
        "When\'s your event happening? Please select the date",
        datetime.date(2023, 4, 1))

    option = col2.selectbox('Please select your prefered booking period',
                    generateDays())

    if st.button('Click to get booking predictions'):
        with st.spinner('Generating predictions. Please wait....'):
            time.sleep(1)
        Company = pd.DataFrame.from_dict([{"StartDate": d}])
        Company['StartDate'] = pd.to_datetime(d, errors='coerce')

        weeks_df = pd.DataFrame(generateWeeksData(pd.to_datetime(d, errors='coerce'), option))
        weeks_df_predict = predictWeekyBookings(weeks_df)

        st.balloons()

        totalBookings = weeks_df_predict['Booking Predictions'].sum()
        st.success("Based on your selected booking period of "+ str(option) +
                   " weeks, the total number of preditcted bookings for your event is: " + str(totalBookings), icon="ℹ️")

        with st.container():
            # col1, col2 = st.columns(2)
            st.info("Weekly booking predictions")
            st.dataframe(weeks_df_predict, use_container_width=True)
            st.info("A plotting of the weekly booking predictions")
            st.line_chart(weeks_df_predict, x='Booking Weeks', y='Booking Predictions')
