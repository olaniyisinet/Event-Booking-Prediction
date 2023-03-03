import streamlit as st
import pandas as pd
import numpy as np
from sklearn import preprocessing

st.set_page_config(layout = "wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Future Event Predictions</h1>", unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align: center;'>Collaborative App Development Coursework</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Predict the booking for your future events using our trained AI model</h5>", unsafe_allow_html=True)


def event_features(dfs):
    """
    Create time series features based on time series index.
    """
    dfs = dfs.copy()
    dfs['eventdayofweek'] = dfs.StartDate.dt.dayofweek
    dfs['eventquarter'] = dfs.StartDate.dt.quarter
    dfs['eventmonth'] = dfs.StartDate.dt.month
    dfs['eventyear'] = dfs.StartDate.dt.year
    dfs['eventdayofyear'] = dfs.StartDate.dt.dayofyear
    dfs['eventdayofmonth'] = dfs.StartDate.dt.day
    dfs['eventweekofyear'] = dfs.StartDate.dt.isocalendar().week
    return dfs

def booking_features(dfs):
    """
    Create time series features based on time series index.
    """
    dfs = dfs.copy()
    dfs['bookingdayofweek'] = dfs.StatusCreatedDate.dt.dayofweek
    dfs['bookingquarter'] = dfs.StatusCreatedDate.dt.quarter
    dfs['bookingmonth'] = dfs.StatusCreatedDate.dt.month
    dfs['bookingyear'] = dfs.StatusCreatedDate.dt.year
    dfs['bookingdayofyear'] = dfs.StatusCreatedDate.dt.dayofyear
    dfs['bookingdayofmonth'] = dfs.StatusCreatedDate.dt.day
    dfs['bookingweekofyear'] = dfs.StatusCreatedDate.dt.isocalendar().week
    return dfs


def CompanyData():
    # Imported CompanyA.csv
    CompanyA = pd.read_csv('DatasetA.csv')
    CompanyC = pd.read_csv('DatasetC.csv')
    CompanyA = CompanyA[CompanyA['BookingStatus'] == 'Attending']
    CompanyC = CompanyC[CompanyC['BookingStatus'] == 'Registered']
    Company = pd.concat([CompanyA, CompanyC])

    #Formating and adding new columns to the dataset
    Company['StatusCreatedDate'] = pd.to_datetime(Company['StatusCreatedDate'], infer_datetime_format=True)
    Company['StartDate'] = pd.to_datetime(Company['StartDate'], infer_datetime_format=True)
    Company['bookingDaysToEvent'] = abs((Company['StartDate'] - Company['StatusCreatedDate']).dt.days)
    Company['bookingWeeksToEvent'] = round(Company['bookingDaysToEvent']/7,0)

    # To create Season column
    _condition_winter = (Company.StartDate.dt.month>=1)&(Company.StartDate.dt.month<=3)
    _condtion_spring = (Company.StartDate.dt.month>=4)&(Company.StartDate.dt.month<=6)
    _condition_summer = (Company.StartDate.dt.month>=7)&(Company.StartDate.dt.month<=9)
    _condition_autumn = (Company.StartDate.dt.month>=10)&(Company.StartDate.dt.month<=12)

    Company['EventSeason'] = np.where(_condition_winter,'Winter',np.where(_condtion_spring,'Spring',np.where(_condition_summer,'Summer',np.where(_condition_autumn,'Autumn',np.nan))))
    #Encoding the season
    encode = preprocessing.LabelEncoder()
    Company['SeasonCode'] = encode.fit_transform(Company['EventSeason'])
    Company = booking_features(Company)
    Company = event_features(Company)
    return Company    







