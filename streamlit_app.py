import streamlit as st
from datetime import datetime, timedelta, timezone
from const.generic import *
from const.queries import *

st.title("PixelWeather Demo Dashboard")
st.write(
    "Note that this app is for demonstration purposes only! _Thanks for checking out anyway!_"
)

# PG connection
conn = st.connection("pwmp-db", type="sql")

# Node Selector
nodes = conn.query(SELECT_NODES)
flex = st.container(horizontal=True, horizontal_alignment="right")
selected_node = flex.selectbox("Node", nodes, help="Pick a node")
time_frame = flex.selectbox("Time frame", SELECTABLE_TIME_FRAMES.keys(), help="Pick a time frame")

# Temperature & Humidity graphs
cutoff = datetime.now(timezone.utc) - SELECTABLE_TIME_FRAMES[time_frame]
df = conn.query(SELECT_MEASUREMENTS, ttl="10m", params={"node": selected_node, "cutoff": cutoff})
st.write(f"Available data points: {len(df)}")
st.line_chart(df, height=250, x="when", y="temperature", x_label="Date&Time", y_label="Temperature [°C]", color="green")
st.line_chart(df, height=250, x="when", y="humidity"   , x_label="Date&Time", y_label="Humidity [%]")

# Battery graph
st.line_chart(df, height=250, x="when", y="battery", x_label="Date&Time", y_label="Battery [V]", color="yellow")

st.divider()
st.write("_(C) pixelweather 2026_")