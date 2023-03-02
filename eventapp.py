import streamlit as st
import pandas as pd
import numpy as np
import altair as alt



st.markdown("<h1 style='text-align: center;'>Group 5</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Collaborative App Development Coursework</h3>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center; color: green'>Exploratory data analysis of previous events</h5>", unsafe_allow_html=True)


def DataSetA():
    CompanyA = pd.read_csv('DatasetA.csv')
    CompanyA = CompanyA[CompanyA['BookingStatus'] == 'Attending']
    CompanyA['StatusCreatedDate'] = pd.to_datetime(CompanyA['StatusCreatedDate'], infer_datetime_format=True)
    CompanyA['StartDate'] = pd.to_datetime(CompanyA['StartDate'], infer_datetime_format=True)
    CompanyA['PurchaseDaysToEvent'] = abs((CompanyA['StartDate'] - CompanyA['StatusCreatedDate']).dt.days)
    CompanyA['PurchaseWeeksToEvent'] = round(CompanyA['PurchaseDaysToEvent']/7,0)
    CompanyA['purchaseweeknumber'] =  CompanyA['eventWeeknumber'] = CompanyA.StatusCreatedDate.dt.isocalendar().week
    CompanyA['eventWeeknumber'] = CompanyA.StartDate.dt.isocalendar().week

        # To create Season column
    _condition_winter = (CompanyA.StartDate.dt.month>=1)&(CompanyA.StartDate.dt.month<=3)
    _condtion_spring = (CompanyA.StartDate.dt.month>=4)&(CompanyA.StartDate.dt.month<=6)
    _condition_summer = (CompanyA.StartDate.dt.month>=7)&(CompanyA.StartDate.dt.month<=9)
    _condition_autumn = (CompanyA.StartDate.dt.month>=10)&(CompanyA.StartDate.dt.month<=12)

    CompanyA['EventSeason'] = np.where(_condition_winter,'Winter',np.where(_condtion_spring,'Spring',np.where(_condition_summer,'Summer',np.where(_condition_autumn,'Autumn',np.nan))))

    return CompanyA


Seaons_df = DataSetA().groupby(['EventType', 'EventSeason', 'EventId', 'PurchaseWeeksToEvent']).aggregate({'GroupSize':'sum'}).reset_index()

def summaryDF():
    min_result = DataSetA().groupby(['EventType', 'EventSeason', 'EventId']).aggregate({'GroupSize':'sum','PurchaseWeeksToEvent':'min'}).reset_index()
    min_result.columns = ['EventType', 'Season','EventId', 'TotalTickets', 'LastPurchaseWeek']

    max_result = DataSetA().groupby(['EventType','EventSeason', 'EventId']).aggregate({'GroupSize':'sum', 'PurchaseWeeksToEvent':'max'}).reset_index()
    max_result.columns = ['EventType2', 'Season2',  'EventId2', 'TotalTickets2', 'FirstPurchaseWeek']

    result_df = pd.concat([min_result, max_result], axis=1, join="inner")

    result_df['TotalWeeksToSell'] = result_df['FirstPurchaseWeek'] - result_df['LastPurchaseWeek']
    result_df.drop(columns=['EventType2', 'TotalTickets2', 'Season2',  'EventId2'], inplace=True)
    
    return result_df





# st.line_chart(result_df, x="StartDate", y="TotalTickets")
# st.line_chart(data=df, x=df['S'].all(),  y=df['GroupSize'].all, width=0, height=0, use_container_width=True)

# st.line_chart(data=None,  x=None, y=None, width=0, height=0, use_container_width=True)


def seasonPlots():
    #Plotting average ticket purchase per season
    Autumn_df = Seaons_df[Seaons_df['EventSeason'] == 'Autumn'].groupby('PurchaseWeeksToEvent').mean().reset_index()
    Autumn_df.columns = ['Weeks to event', 'EventId', 'Bookings']
    Spring_df = Seaons_df[Seaons_df['EventSeason'] == 'Spring'].groupby('PurchaseWeeksToEvent').mean().reset_index()
    Spring_df.columns = ['Weeks to event', 'EventId', 'Bookings']
    Summer_df = Seaons_df[Seaons_df['EventSeason'] == 'Summer'].groupby('PurchaseWeeksToEvent').mean().reset_index()
    Summer_df.columns = ['Weeks to event', 'EventId', 'Bookings']
    Winter_df = Seaons_df[Seaons_df['EventSeason'] == 'Winter'].groupby('PurchaseWeeksToEvent').mean().reset_index()
    Winter_df.columns = ['Weeks to event', 'EventId', 'Bookings']

# event_df = Seaons_df[Seaons_df['EventType'] == event].groupby('PurchaseWeeksToEvent').mean()

# st.table(Autumn_df)
    st.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Autumn events</h5>", unsafe_allow_html=True)
    st.line_chart(Autumn_df, x="Weeks to event", y="Bookings", use_container_width=True)

    st.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Spring events</h5>", unsafe_allow_html=True)
    st.line_chart(Spring_df, x="Weeks to event", y="Bookings", use_container_width=True)

    st.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Summer events</h5>", unsafe_allow_html=True)
    st.line_chart(Summer_df, x="Weeks to event", y="Bookings", use_container_width=True)

    st.markdown("<h5 style='text-align: center; color: red'>Average weekly bookings for Winter events</h5>", unsafe_allow_html=True)
    st.line_chart(Winter_df, x="Weeks to event", y="Bookings", use_container_width=True)


    # df = pd.DataFrame(
    # {
    #     'Weeks to event': Autumn_df['Weeks to event'],
    #     'Autumn Bookings': round(Autumn_df['Autumn Bookings']),
    #     'Spring Bookings': round(Spring_df['Spring Bookings']),
    #     'Summer Bookings': round(Summer_df['Summer Bookings']),
    #     'Winter Bookings': round(Winter_df['Winter Bookings']),
    # },
    # columns=['Autumn Bookings', 'Spring Bookings', 'Summer Bookings', 'Winter Bookings']
    # )
   
    # st.line_chart(df)

    # chart = alt.Chart(df).mark_line().encode(
    # x=alt.X('Weeks to event'),
    # y=alt.Y('Autumn Bookings'),
    # y=alt.Y('Spring Bookings'),
    # y=alt.Y('Summer Bookings'),
    # color=alt.Color("name:N")
    # ).properties(title="Hello World")

    # st.altair_chart(chart, use_container_width=True)

# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c'])

# st.line_chart(chart_data)

seasonPlots()
