import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout = "wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Dataset C</h1>", unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align: center;'>Collaborative App Development Coursework</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Exploratory data analysis of previous events in Dataset C</h5>", unsafe_allow_html=True)


@st.cache_data
def DataSetC():
    CompanyC = pd.read_csv('DatasetC.csv')
    CompanyC = CompanyC[CompanyC['BookingStatus'] == 'Registered']
    CompanyC['StatusCreatedDate'] = pd.to_datetime(CompanyC['StatusCreatedDate'], infer_datetime_format=True)
    CompanyC['StartDate'] = pd.to_datetime(CompanyC['StartDate'], infer_datetime_format=True)
    CompanyC['BookingDaysToEvent'] = abs((CompanyC['StartDate'] - CompanyC['StatusCreatedDate']).dt.days)
    CompanyC['BookingWeeksToEvent'] = round(CompanyC['BookingDaysToEvent']/7,0)
    CompanyC['Bookingweeknumber'] =  CompanyC['eventWeeknumber'] = CompanyC.StatusCreatedDate.dt.isocalendar().week
    CompanyC['eventWeeknumber'] = CompanyC.StartDate.dt.isocalendar().week

        # To create Season column
    _condition_winter = (CompanyC.StartDate.dt.month>=1)&(CompanyC.StartDate.dt.month<=3)
    _condtion_spring = (CompanyC.StartDate.dt.month>=4)&(CompanyC.StartDate.dt.month<=6)
    _condition_summer = (CompanyC.StartDate.dt.month>=7)&(CompanyC.StartDate.dt.month<=9)
    _condition_autumn = (CompanyC.StartDate.dt.month>=10)&(CompanyC.StartDate.dt.month<=12)

    CompanyC['EventSeason'] = np.where(_condition_winter,'Winter',np.where(_condtion_spring,'Spring',np.where(_condition_summer,'Summer',np.where(_condition_autumn,'Autumn',np.nan))))

    return CompanyC


Seaons_df = DataSetC().groupby(['EventSeason', 'EventId', 'BookingWeeksToEvent']).aggregate({'GroupSize':'sum'}).reset_index()
# st.table(Seaons_df)

def summaryDF():
    min_result = DataSetC().groupby(['EventSeason', 'EventId']).aggregate({'GroupSize':'sum','BookingWeeksToEvent':'min'}).reset_index()
    min_result.columns = [ 'Season','EventId', 'TotalTickets', 'LastBookingWeek']

    max_result = DataSetC().groupby(['EventSeason', 'EventId']).aggregate({'GroupSize':'sum', 'BookingWeeksToEvent':'max'}).reset_index()
    max_result.columns = ['Season2',  'EventId2', 'TotalTickets2', 'FirstBookingWeek']

    result_df = pd.concat([min_result, max_result], axis=1, join="inner")

    result_df['TotalWeeksToSell'] = result_df['FirstBookingWeek'] - result_df['LastBookingWeek']
    result_df.drop(columns=['TotalTickets2', 'Season2',  'EventId2'], inplace=True)
    
    return result_df


def Autumn():
    #Plotting average ticket Booking per season
    Autumn_df = Seaons_df[Seaons_df['EventSeason'] == 'Autumn'].groupby('BookingWeeksToEvent').mean().reset_index()
    Autumn_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Autumn_df

def Spring():
    Spring_df = Seaons_df[Seaons_df['EventSeason'] == 'Spring'].groupby('BookingWeeksToEvent').mean().reset_index()
    Spring_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Spring_df

def Summer():
    Summer_df = Seaons_df[Seaons_df['EventSeason'] == 'Summer'].groupby('BookingWeeksToEvent').mean().reset_index()
    Summer_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Summer_df

def Winter():
    Winter_df = Seaons_df[Seaons_df['EventSeason'] == 'Winter'].groupby('BookingWeeksToEvent').mean().reset_index()
    Winter_df.columns = ['Weeks to event', 'EventId', 'Average Bookings']
    return Winter_df

# event_df = Seaons_df[Seaons_df['EventType'] == event].groupby('BookingWeeksToEvent').mean()

# st.table(Autumn_df)
with st.container():
    # st.header('Streamlit Colour Picker for Charts')
    # user_colour = st.color_picker(label='Choose a colour for your plot')
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
    col1, col2 = st.columns(2, gap="large")
    col1.subheader("Average first booking week per season") 
    col1.info("What is the average time it taskes for bookings to start per season?") 
    first_Booking = summaryDF().groupby(['Season']).aggregate({'FirstBookingWeek':'mean'}).reset_index()
    # st.table(first_Booking)
    first_Booking['FirstBookingWeek'] = round(first_Booking['FirstBookingWeek'])
    first_Booking.columns = ['Season', 'Average First Booking Week']
    col1.bar_chart(first_Booking, x='Season', y='Average First Booking Week')

    col2.subheader("Average lask booking week per season")  
    col2.info("What is the average week number for the last booking?") 
    last_Booking = summaryDF().groupby(['Season']).aggregate({'LastBookingWeek':'mean'}).reset_index()
    # st.table(first_Booking)
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

# with st.container():
#     chart = (
#     alt.Chart(summaryDF())
#     .mark_bar()
#     .encode(
#         alt.X("Season:O"),
#         alt.Y("TotalWeeksToSell"),
#         alt.Color("Nucleotide:O"),
#         alt.Tooltip(["Season", "TotalWeeksToSell"]),
#     )
#     .interactive()
# )
# st.altair_chart(chart)


st.table(DataSetC())
st.button("Re-run")