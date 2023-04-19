#This page contains the summary and brief description of the other pages.

import streamlit as st

st.set_page_config(layout = "wide")

st.markdown("<h1 style='text-align: center;'>Group 5 Collaborative App Development Project 👋</h1>", unsafe_allow_html=True)
st.sidebar.success("Select a menu above.")
st.markdown("<h5 style='text-align: center; color: green'> This is group 5's approach to answering the client's question and attempt to providing a solution to the challenge.</h5> <br><br>", unsafe_allow_html=True)
st.markdown(
    """
    **👈 Select a menu from the side** to see some of the analysis we have gathered from each dataset!

    ### What each menu will display?

    - Dataset A: Charts, graphs, and explaination of what dataset A contains and it can be useful.
    - Dataset B: Charts, graphs, and explaination of what dataset B contains and it can be useful.
    - Dataset C: Charts, graphs, and explaination of what dataset C contains and it can be useful.
    - Event Prediction: Prediction furture events with our trained model from the dataset provided.
    - Client Prefered Prediction: Prediction furture events givign the client the ability to select a prefered booking period.

"""
)
