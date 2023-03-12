#This page contains the exploratory data analysis of dataset B. It contains graphs and charts explains the trends and pattern in the given dataset.

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

#Setting page layout
st.set_page_config(layout = "wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Dataset B</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Exploratory data analysis of previous events in Dataset B</h5>", unsafe_allow_html=True)


@st.cache_data
def DataSetB():
    CompanyB = pd.read_csv('DatasetB.csv')
    CompanyB = CompanyB[CompanyB['BookingStatus'] == 'Attending']
    CompanyB['StatusCreatedDate'] = pd.to_datetime(CompanyB['StatusCreatedDate'], infer_datetime_format=True)
    CompanyB['StartDate'] = pd.to_datetime(CompanyB['StartDate'], infer_datetime_format=True)
    CompanyB['BookingDaysToEvent'] = abs((CompanyB['StartDate'] - CompanyB['StatusCreatedDate']).dt.days)
    CompanyB['BookingWeeksToEvent'] = round(CompanyB['BookingDaysToEvent']/7,0)
    CompanyB['Bookingweeknumber'] = CompanyB.StatusCreatedDate.dt.isocalendar().week
    CompanyB['eventWeeknumber'] = CompanyB.StartDate.dt.isocalendar().week

    #To create Season column
    _condition_winter = (CompanyB.StartDate.dt.month>=1)&(CompanyB.StartDate.dt.month<=3)
    _condtion_spring = (CompanyB.StartDate.dt.month>=4)&(CompanyB.StartDate.dt.month<=6)
    _condition_summer = (CompanyB.StartDate.dt.month>=7)&(CompanyB.StartDate.dt.month<=9)
    _condition_autumn = (CompanyB.StartDate.dt.month>=10)&(CompanyB.StartDate.dt.month<=12)

    CompanyB['EventSeason'] = np.where(_condition_winter,'Winter',np.where(_condtion_spring,'Spring',np.where(_condition_summer,'Summer',np.where(_condition_autumn,'Autumn',np.nan))))

    #Cleaining up the ticket type
    CompanyB['TicketType']=CompanyB['TicketType'].replace('AM Ceremony','Standard')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Child (AM ceremony)','Child Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Child (PM ceremony)','Child Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Evening dinner ','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Guest AM Ceremony','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Guest PM Ceremony','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('PM Ceremony ','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('PM Ceremony','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('121 Session','Standard')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('14:30 Ceremony','Standard')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('11:00 Ceremony','Standard')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Guest 14:30 Ceremony','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Guest 17:00 Ceremony','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Guest 11:00 Ceremony','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('17:00 Ceremony','Standard')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('13th Ceremony','Standard')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('14th Ceremony','Standard')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('15th Ceremony','Standard')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Guest 13th Ceremony','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Guest 14th Ceremony','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Guest 15th Ceremony','Adult Guest')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('3 day ticket am/pm','Standard')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Academic Ticket','Academic Staff')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Teaching Centre Staff','Academic Staff')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Any day', 'Standard')
    CompanyB['TicketType']=CompanyB['TicketType'].replace('Standard', 'Graudants')

    return CompanyB

Seaons_df = DataSetB().groupby(['EventSeason', 'EventId', 'BookingWeeksToEvent', 'TicketType']).aggregate({'GroupSize':'count'}).reset_index()

def summaryDF():
    min_result = DataSetB().groupby([ 'EventSeason', 'EventId', 'TicketType']).aggregate({'GroupSize':'sum','BookingWeeksToEvent':'min'}).reset_index()
    min_result.columns = [ 'Season','EventId', 'TicketType','TotalBookings', 'LastBookingWeek']
    max_result = DataSetB().groupby(['EventSeason', 'EventId', 'TicketType']).aggregate({'GroupSize':'sum', 'BookingWeeksToEvent':'max'}).reset_index()
    max_result.columns = ['Season2',  'EventId2', 'TicketType2', 'TotalTickets2', 'FirstBookingWeek']
    result_df = pd.concat([min_result, max_result], axis=1, join="inner")
    result_df['TotalBookingWeeks'] = result_df['FirstBookingWeek'] - result_df['LastBookingWeek']
    result_df.drop(columns=['TicketType2', 'TotalTickets2', 'Season2',  'EventId2'], inplace=True)

    return result_df


def Graduants():
    #Plotting average ticket type Booking
    Graudants_df = Seaons_df[Seaons_df['TicketType'] == 'Graudants'].groupby('BookingWeeksToEvent').mean().reset_index()
    Graudants_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Graudants_df
   
def Child_Guest():
    Child_Guest_df = Seaons_df[Seaons_df['TicketType'] == 'Child Guest'].groupby('BookingWeeksToEvent').mean().reset_index()
    Child_Guest_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Child_Guest_df

def Adult_Guest():
    Adult_Guest_df = Seaons_df[Seaons_df['TicketType'] == 'Adult Guest'].groupby('BookingWeeksToEvent').mean().reset_index()
    Adult_Guest_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Adult_Guest_df

def Academic_Staff():
    Academic_Staff_df = Seaons_df[Seaons_df['TicketType'] == 'Academic Staff'].groupby('BookingWeeksToEvent').mean().reset_index()
    Academic_Staff_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Academic_Staff_df


with st.container():

    st.subheader("Average Booking by Ticket Types")  
    st.info("What are the average number of bookings for each week before the event for every attendee type?") 

    col1, col2 = st.columns(2, gap="large")

    col1.markdown("<h5 style='text-align: center; color: red'>Average graduants bookings per weeks to events</h5>", unsafe_allow_html=True)
    col1.line_chart(Graduants(), x="Weeks to event", y="Average Bookings", use_container_width=True)

    col1.markdown("<h5 style='text-align: center; color: red'>Average child guest bookings per weeks to events</h5>", unsafe_allow_html=True)
    col1.line_chart(Child_Guest(), x="Weeks to event", y="Average Bookings", use_container_width=True)

    col2.markdown("<h5 style='text-align: center; color: red'>Average adult guest bookings per weeks to events</h5>", unsafe_allow_html=True)
    col2.line_chart(Adult_Guest(), x="Weeks to event", y="Average Bookings", use_container_width=True)

    col2.markdown("<h5 style='text-align: center; color: red'>Average academic staff bookings per weeks to events</h5>", unsafe_allow_html=True)
    col2.line_chart(Academic_Staff(), x="Weeks to event", y="Average Bookings", use_container_width=True)


with st.container():
    col1, col2 = st.columns(2, gap="large")
    col1.subheader("Average first booking week per season") 
    col1.info("What is the average time it taskes for bookings to start per season?") 

    first_Booking = summaryDF().groupby(['TicketType']).aggregate({'FirstBookingWeek':'mean'}).reset_index()
    first_Booking['FirstBookingWeek'] = round(first_Booking['FirstBookingWeek'])
    first_Booking.columns = ['Ticket Type', 'Average First Booking Week']
    col1.bar_chart(first_Booking, x='Ticket Type', y='Average First Booking Week')

    col2.subheader("Average last booking week per season")  
    col2.info("What is the average week number for the last booking?") 

    last_Booking = summaryDF().groupby(['Season']).aggregate({'LastBookingWeek':'mean'}).reset_index()
    last_Booking['LastBookingWeek'] = round(last_Booking['LastBookingWeek'])
    last_Booking.columns = ['Ticket Type', 'Average Last Booking Week']
    col2.bar_chart(last_Booking, x='Ticket Type', y='Average Last Booking Week')


with st.container():
    st.subheader("Average booking weeks per tickets type")  
    st.info("What is the average number of booking weeks per season?") 
    total_Booking = summaryDF().groupby(['TicketType']).aggregate({'TotalBookingWeeks':'mean'}).reset_index()
    total_Booking['TotalBookingWeeks'] = round(total_Booking['TotalBookingWeeks'])
    total_Booking.columns = ['Ticket Type', 'Average Booking Weeks']
    st.bar_chart(total_Booking, x='Ticket Type', y='Average Booking Weeks')

st.button("Re-run")