import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

st.title("Explore Austin's Animal Shelter Data")

df = pd.read_csv("Intakes_2021_withlocationdetails.csv", parse_dates=['DateTime'])

date_min, date_max = st.date_input(label="What time frame would you like to explore?", 
                                   value=[date(2021, 1, 1), date(2021, 6, 9)], 
                                   min_value=date(2021, 1, 1),
                                   max_value=date(2021, 6, 9))

date_min = pd.to_datetime(date_min)
date_max = pd.to_datetime(date_max)

sub_df = df.loc[(df['DateTime'] <= date_max) &
                (df['DateTime'] >= date_min)]

sub_df = sub_df[~sub_df['found_lat'].isna()]

viz_df = sub_df.groupby(['Found Location', 'found_lat', 'found_lon']).count()[
    'Animal ID'].reset_index()

viz_df = viz_df.rename(columns={'Animal ID': 'count'})

st.write("### Found Locations of Animals in that Time Frame:")

fig = px.scatter_mapbox(
    viz_df,
    lat='found_lat',
    lon='found_lon',
    size="count",
    color='count',
    hover_name="Found Location",
    zoom=9,
)
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0},
    mapbox=dict(
        center={'lat': 30.2672, 'lon': -97.7431},
    )
)
st.plotly_chart(fig)