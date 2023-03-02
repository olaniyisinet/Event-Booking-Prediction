import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

st.set_page_config(layout = "wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Dataset A</h1>", unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align: center;'>Collaborative App Development Coursework</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: green'>Exploratory data analysis of previous events in Dataset A</h5>", unsafe_allow_html=True)


@st.cache_data
def DataSetA():
    CompanyA = pd.read_csv('DatasetA.csv')
    CompanyA = CompanyA[CompanyA['BookingStatus'] == 'Attending']
    CompanyA['StatusCreatedDate'] = pd.to_datetime(CompanyA['StatusCreatedDate'], infer_datetime_format=True)
    CompanyA['StartDate'] = pd.to_datetime(CompanyA['StartDate'], infer_datetime_format=True)
    CompanyA['BookingDaysToEvent'] = abs((CompanyA['StartDate'] - CompanyA['StatusCreatedDate']).dt.days)
    CompanyA['BookingWeeksToEvent'] = round(CompanyA['BookingDaysToEvent']/7,0)
    CompanyA['Bookingweeknumber'] =  CompanyA['eventWeeknumber'] = CompanyA.StatusCreatedDate.dt.isocalendar().week
    CompanyA['eventWeeknumber'] = CompanyA.StartDate.dt.isocalendar().week

        # To create Season column
    _condition_winter = (CompanyA.StartDate.dt.month>=1)&(CompanyA.StartDate.dt.month<=3)
    _condtion_spring = (CompanyA.StartDate.dt.month>=4)&(CompanyA.StartDate.dt.month<=6)
    _condition_summer = (CompanyA.StartDate.dt.month>=7)&(CompanyA.StartDate.dt.month<=9)
    _condition_autumn = (CompanyA.StartDate.dt.month>=10)&(CompanyA.StartDate.dt.month<=12)

    CompanyA['EventSeason'] = np.where(_condition_winter,'Winter',np.where(_condtion_spring,'Spring',np.where(_condition_summer,'Summer',np.where(_condition_autumn,'Autumn',np.nan))))

    return CompanyA


Seaons_df = DataSetA().groupby(['EventType', 'EventSeason', 'EventId', 'BookingWeeksToEvent']).aggregate({'GroupSize':'sum'}).reset_index()
# st.table(Seaons_df)

def summaryDF():
    min_result = DataSetA().groupby(['EventType', 'EventSeason', 'EventId']).aggregate({'GroupSize':'sum','BookingWeeksToEvent':'min'}).reset_index()
    min_result.columns = ['EventType', 'Season','EventId', 'TotalTickets', 'LastBookingWeek']

    max_result = DataSetA().groupby(['EventType','EventSeason', 'EventId']).aggregate({'GroupSize':'sum', 'BookingWeeksToEvent':'max'}).reset_index()
    max_result.columns = ['EventType2', 'Season2',  'EventId2', 'TotalTickets2', 'FirstBookingWeek']

    result_df = pd.concat([min_result, max_result], axis=1, join="inner")

    result_df['TotalWeeksToSell'] = result_df['FirstBookingWeek'] - result_df['LastBookingWeek']
    result_df.drop(columns=['EventType2', 'TotalTickets2', 'Season2',  'EventId2'], inplace=True)
    
    return result_df


def Autumn():
    #Plotting average ticket Booking per season
    Autumn_df = Seaons_df[Seaons_df['EventSeason'] == 'Autumn'].groupby('BookingWeeksToEvent').mean().reset_index()
    Autumn_df.columns = ['Weeks to event', 'EventId', 'Bookings']
    return Autumn_df

def Spring():
    Spring_df = Seaons_df[Seaons_df['EventSeason'] == 'Spring'].groupby('BookingWeeksToEvent').mean().reset_index()
    Spring_df.columns = ['Weeks to event', 'EventId', 'Bookings']
    return Spring_df

def Summer():
    Summer_df = Seaons_df[Seaons_df['EventSeason'] == 'Summer'].groupby('BookingWeeksToEvent').mean().reset_index()
    Summer_df.columns = ['Weeks to event', 'EventId', 'Bookings']
    return Summer_df

def Winter():
    Winter_df = Seaons_df[Seaons_df['EventSeason'] == 'Winter'].groupby('BookingWeeksToEvent').mean().reset_index()
    Winter_df.columns = ['Weeks to event', 'EventId', 'Bookings']
    return Winter_df

# event_df = Seaons_df[Seaons_df['EventType'] == event].groupby('BookingWeeksToEvent').mean()

# st.table(Autumn_df)
with st.container():
    # st.header('Streamlit Colour Picker for Charts')

    # user_colour = st.color_picker(label='Choose a colour for your plot')
    col1, col2 = st.columns(2, gap="large")

    col1.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Autumn events</h5>", unsafe_allow_html=True)
    col1.line_chart(Autumn(), x="Weeks to event", y="Bookings", use_container_width=True)

    col1.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Spring events</h5>", unsafe_allow_html=True)
    col1.line_chart(Spring(), x="Weeks to event", y="Bookings", use_container_width=True)

    col2.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Summer events</h5>", unsafe_allow_html=True)
    col2.line_chart(Summer(), x="Weeks to event", y="Bookings", use_container_width=True)

    col2.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Winter events</h5>", unsafe_allow_html=True)
    col2.line_chart(Winter(), x="Weeks to event", y="Bookings", use_container_width=True)


with st.container():
    st.header("Average weekly Booking by event type")  
    st.info("Select a single event type to see the distribution")

    eventsTypes = list(Seaons_df['EventType'].unique())
    tablable = eventsTypes
    # tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs(eventsTypes)

    tablable = st.tabs(eventsTypes)

    tabint = 0
    for id, event in enumerate(eventsTypes):
        event_df = Seaons_df[Seaons_df['EventType'] == event].groupby('BookingWeeksToEvent').mean().reset_index()
        event_df.columns = ['Weeks To Event', 'EventId', 'Group Size']
        event_df['Weeks To Event'] = round(event_df['Weeks To Event'],0)
        # st.table(event_df)
        # print(tabs)
        tablable[id].markdown("<h5 style='text-align: left; color: blue'>Average weekly bookings for " +event+"</h5>", unsafe_allow_html=True)

        # fig, ax = plt.subplots()
        # ax.lines(x=event_df['Weeks To Event'], y=event_df['Group Size'], c=user_colour)
        # tablable[id].pyplot(fig)

        tablable[id].line_chart(event_df, x="Weeks To Event", y="Group Size", use_container_width=True)
        # tabint+1 

with st.container():
    st.header("Average first week purchase")  
    first_Booking = summaryDF().groupby(['Season']).aggregate({'FirstBookingWeek':'mean'}).reset_index()
    first_Booking['FirstBookingWeek'] = round(first_Booking['FirstBookingWeek'])
    st.bar_chart(first_Booking, x='Season', y='FirstBookingWeek')

with st.container():
    chart = (
    alt.Chart(summaryDF())
    .mark_bar()
    .encode(
        alt.X("Season:O"),
        alt.Y("TotalWeeksToSell"),
        alt.Color("Nucleotide:O"),
        alt.Tooltip(["Season", "TotalWeeksToSell"]),
    )
    .interactive()
)
st.altair_chart(chart)

st.button("Re-run")