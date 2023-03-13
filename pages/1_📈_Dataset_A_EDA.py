#This page contains the exploratory data analysis of dataset A. It contains graphs and charts explains the trends and pattern in the given dataset.

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

#Setting page layout
st.set_page_config(layout = "wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Dataset A</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Exploratory data analysis of previous events in Dataset A</h5>", unsafe_allow_html=True)


#Connecting to the data source csv, pre-processing and generating the data frame for visualisation
@st.cache_data
def DataSetA():
    CompanyA = pd.read_csv('DatasetA.csv')
    CompanyA = CompanyA[CompanyA['BookingStatus'] == 'Attending']
    CompanyA['StatusCreatedDate'] = pd.to_datetime(CompanyA['StatusCreatedDate'], infer_datetime_format=True)
    CompanyA['StartDate'] = pd.to_datetime(CompanyA['StartDate'], infer_datetime_format=True)
    CompanyA['BookingDaysToEvent'] = abs((CompanyA['StartDate'] - CompanyA['StatusCreatedDate']).dt.days)
    CompanyA['BookingWeeksToEvent'] = round(CompanyA['BookingDaysToEvent']/7,0)
    CompanyA['Bookingweeknumber'] =  CompanyA.StatusCreatedDate.dt.isocalendar().week
    CompanyA['eventWeeknumber'] = CompanyA.StartDate.dt.isocalendar().week

    # To create Season column
    _condition_winter = (CompanyA.StartDate.dt.month>=1)&(CompanyA.StartDate.dt.month<=3)
    _condtion_spring = (CompanyA.StartDate.dt.month>=4)&(CompanyA.StartDate.dt.month<=6)
    _condition_summer = (CompanyA.StartDate.dt.month>=7)&(CompanyA.StartDate.dt.month<=9)
    _condition_autumn = (CompanyA.StartDate.dt.month>=10)&(CompanyA.StartDate.dt.month<=12)

    CompanyA['EventSeason'] = np.where(_condition_winter,'Winter',np.where(_condtion_spring,'Spring',np.where(_condition_summer,'Summer',np.where(_condition_autumn,'Autumn',np.nan))))

    return CompanyA


#Extracting grouped data for season, event types, and booking weeks to event
Seaons_df = DataSetA().groupby(['EventType', 'EventSeason', 'EventId', 'BookingWeeksToEvent']).aggregate({'GroupSize':'sum'}).reset_index()


#Extracting grouped data for season and event types
def summaryDF():
    min_result = DataSetA().groupby(['EventType', 'EventSeason', 'EventId']).aggregate({'GroupSize':'sum','BookingWeeksToEvent':'min'}).reset_index()
    min_result.columns = ['EventType', 'Season','EventId', 'TotalTickets', 'LastBookingWeek']

    max_result = DataSetA().groupby(['EventType','EventSeason', 'EventId']).aggregate({'GroupSize':'sum', 'BookingWeeksToEvent':'max'}).reset_index()
    max_result.columns = ['EventType2', 'Season2',  'EventId2', 'TotalTickets2', 'FirstBookingWeek']

    result_df = pd.concat([min_result, max_result], axis=1, join="inner")

    result_df['TotalWeeksToSell'] = result_df['FirstBookingWeek'] - result_df['LastBookingWeek']
    result_df.drop(columns=['EventType2', 'TotalTickets2', 'Season2',  'EventId2'], inplace=True)
    
    return result_df


#Creating a DF for average bookings in Autumn
def Autumn():
    Autumn_df = Seaons_df[Seaons_df['EventSeason'] == 'Autumn'].groupby('BookingWeeksToEvent').mean().reset_index()
    Autumn_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Autumn_df

#Creating a DF for average bookings in Spring
def Spring():
    Spring_df = Seaons_df[Seaons_df['EventSeason'] == 'Spring'].groupby('BookingWeeksToEvent').mean().reset_index()
    Spring_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Spring_df

#Creating a DF for average bookings in Summer
def Summer():
    Summer_df = Seaons_df[Seaons_df['EventSeason'] == 'Summer'].groupby('BookingWeeksToEvent').mean().reset_index()
    Summer_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Summer_df

#Creating a DF for average bookings in Winter
def Winter():
    Winter_df = Seaons_df[Seaons_df['EventSeason'] == 'Winter'].groupby('BookingWeeksToEvent').mean().reset_index()
    Winter_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Winter_df


#Container to plot all the graphs
with st.container():
    st.subheader("Average Booking by Seasons")  
    st.info("What are the average number of bookings for each week before the event for every season?") 

    col1, col2 = st.columns(2, gap="large")

    col1.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Autumn events</h5>", unsafe_allow_html=True)
    col1.line_chart(Autumn(), x="Weeks to event", y="Average Bookings", use_container_width=True)

    col1.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Spring events</h5>", unsafe_allow_html=True)
    col1.line_chart(Spring(), x="Weeks to event", y="Average Bookings", use_container_width=True)

    col2.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Summer events</h5>", unsafe_allow_html=True)
    col2.line_chart(Summer(), x="Weeks to event", y="Average Bookings", use_container_width=True)

    col2.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Winter events</h5>", unsafe_allow_html=True)
    col2.line_chart(Winter(), x="Weeks to event", y="Average Bookings", use_container_width=True)


with st.container():
    st.subheader("Average weekly Booking by event type")  
    st.info("Select a single event type to see the distribution")

    eventsTypes = list(Seaons_df['EventType'].unique())
    tablable = eventsTypes

    tablable = st.tabs(eventsTypes)

    tabint = 0
    for id, event in enumerate(eventsTypes):
        event_df = Seaons_df[Seaons_df['EventType'] == event].groupby('BookingWeeksToEvent').mean().reset_index()
        event_df.columns = ['Weeks To Event', 'EventId', 'Group Size']
        event_df['Weeks To Event'] = round(event_df['Weeks To Event'],0)
        tablable[id].markdown("<h5 style='text-align: left; color: blue'>Average weekly bookings for " +event+"</h5>", unsafe_allow_html=True)
        tablable[id].line_chart(event_df, x="Weeks To Event", y="Group Size", use_container_width=True)


with st.container():
    col1, col2 = st.columns(2, gap="large")
    col1.subheader("Average first booking week per season") 
    col1.info("What is the average time it taskes for bookings to start per season?") 
    first_Booking = summaryDF().groupby(['Season']).aggregate({'FirstBookingWeek':'mean'}).reset_index()
    first_Booking['FirstBookingWeek'] = round(first_Booking['FirstBookingWeek'])
    first_Booking.columns = ['Season', 'Average First Booking Week']
    col1.bar_chart(first_Booking, x='Season', y='Average First Booking Week')

    col2.subheader("Average last booking week per season")  
    col2.info("What is the average week number for the last booking?") 
    last_Booking = summaryDF().groupby(['Season']).aggregate({'LastBookingWeek':'mean'}).reset_index()
    last_Booking['LastBookingWeek'] = round(last_Booking['LastBookingWeek'])
    last_Booking.columns = ['Season', 'Average Last Booking Week']
    col2.bar_chart(last_Booking, x='Season', y='Average Last Booking Week')


with st.container():
    st.subheader("Average booking weeks per season")  
    st.info("What is the average number of weeks it takes to sell tickets per season?") 
    total_Booking = summaryDF().groupby(['Season']).aggregate({'TotalWeeksToSell':'mean'}).reset_index()
    total_Booking['TotalWeeksToSell'] = round(total_Booking['TotalWeeksToSell'])
    total_Booking.columns = ['Season', 'Average Booking Weeks']
    st.bar_chart(total_Booking, x='Season', y='Average Booking Weeks')

st.button("Re-run")