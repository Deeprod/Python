import streamlit as st
import altair as alt
import importlib

import _util
importlib.reload(_util)  
from _util import *
        
def barchart_movies(df):
    df["Count"] = 1
    df["Date"] = df["Date"].apply(DDMMYYYY_to_MMYY)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df = df.sort_values("Date")

    container = st.container(border = True)
    container.markdown(f"#### {len(df)} movies watched since 2019")
    
    color_scale = alt.Scale(
        domain=[4, 5, 6, 7, 8, 9],  # Replace with your actual team members
        range=["#b41f1f", "#b41f1f", "#bd851e", "#2c55a0", "#2ca053", "#922ca0"]  # Your custom colors
    )

    # Create Altair chart
    bar_chart = alt.Chart(df).mark_bar(size=6).encode(  # Adjust 'size' for bar thickness
        y=alt.Y("Date:T", sort="ascending", title="Date"),
        x=alt.X("Count:Q", title="Count"),
        color=alt.Color("JK Rating:N", scale=color_scale),
        tooltip=["Date", "Name", "JK Rating"]
    ).properties(height=500)
    container.altair_chart(bar_chart, use_container_width=True)