import streamlit as st
import pandas as pd
import numpy as np
from sklearn import preprocessing

st.set_page_config(layout = "wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Correlation Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Correlation analysis was performed on the datasets A and C after they were combined.</h5>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: red'>Dataset B was exlcuded from this analysis as it does not have enough relevant data</h6>", unsafe_allow_html=True)


@st.cache_data
def getDataSet():
    CompanyA = pd.read_csv('DatasetA.csv')
    CompanyC = pd.read_csv('DatasetC.csv', low_memory=False)
    CompanyC = CompanyC[CompanyC['BookingStatus'] == 'Registered']
    CompanyA = CompanyA[CompanyA['BookingStatus'] == 'Attending']
    Company = pd.concat([CompanyA, CompanyC])

    Company['StatusCreatedDate'] = pd.to_datetime(Company['StatusCreatedDate'], infer_datetime_format=True)
    Company['StartDate'] = pd.to_datetime(Company['StartDate'], infer_datetime_format=True)
    Company['BookingDaysToEvent'] = abs((Company['StartDate'] - Company['StatusCreatedDate']).dt.days)
    Company['BookingWeeksToEvent'] = round(Company['BookingDaysToEvent']/7,0)
    Company['Bookingweeknumber'] =  Company['eventWeeknumber'] = Company.StatusCreatedDate.dt.isocalendar().week
    Company['eventWeeknumber'] = Company.StartDate.dt.isocalendar().week

    # To create Season column
    _condition_winter = (Company.StartDate.dt.month>=1)&(Company.StartDate.dt.month<=3)
    _condtion_spring = (Company.StartDate.dt.month>=4)&(Company.StartDate.dt.month<=6)
    _condition_summer = (Company.StartDate.dt.month>=7)&(Company.StartDate.dt.month<=9)
    _condition_autumn = (Company.StartDate.dt.month>=10)&(Company.StartDate.dt.month<=12)

    Company['EventSeason'] = np.where(_condition_winter,'Winter',np.where(_condtion_spring,'Spring',np.where(_condition_summer,'Summer',np.where(_condition_autumn,'Autumn',np.nan))))
    encode = preprocessing.LabelEncoder()
    Company['SeasonCode'] = encode.fit_transform(Company['EventSeason'])
    Company = booking_features(Company)
    Company = event_features(Company)

    min_result = Company.groupby(['StartDate', 'EventSeason', 'SeasonCode', 'EventId']).aggregate({'GroupSize':'sum','BookingWeeksToEvent':'min'}).reset_index()
    min_result.columns = ['StartDate', 'Season', 'SeasonCode', 'EventId', 'TotalTickets', 'LastbookingWeek']
    # print(min_result)

    max_result = Company.groupby(['StartDate','EventSeason', 'SeasonCode', 'EventId']).aggregate({'GroupSize':'sum', 'BookingWeeksToEvent':'max'}).reset_index()
    max_result.columns = ['StartDate2', 'Season2', 'SeasonCode2', 'EventId2', 'TotalTickets2', 'FirstbookingWeek']
    # print(max_result)

    result_df = pd.concat([min_result, max_result], axis=1, join="inner")

    result_df['TotalWeeksToSell'] = result_df['FirstbookingWeek'] - result_df['LastbookingWeek']
    result_df.drop(columns=['StartDate2', 'TotalTickets2', 'Season2', 'SeasonCode2', 'EventId2'], inplace=True)

    result_df['EventDate'] = result_df['StartDate'].dt.date

    result_df = event_features(result_df)
    result_df = result_df.astype({'eventdayofweek': 'int', 'eventquarter':'int', 'eventmonth':'int', 'eventyear':'int' ,'eventdayofyear':'int','eventdayofmonth':'int','eventweekofyear':'int', 'EventId': 'str'})

    return result_df

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

st.dataframe(getDataSet())