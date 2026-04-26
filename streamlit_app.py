import streamlit as st
from datetime import datetime, timezone
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

# Query data
cutoff = datetime.now(timezone.utc) - SELECTABLE_TIME_FRAMES[time_frame]
df = conn.query(SELECT_MEASUREMENTS, ttl="10m", params={"node": selected_node, "cutoff": cutoff})
latest_df = df.iloc[-1]
# Cut the data frames in half
if SELECTABLE_TIME_FRAMES[time_frame].days >= 7:
    df = df.iloc[::2, :]

# Current values
with st.container(border=True):
    timestamp = latest_df["when"].strftime('%Y-%m-%d %H:%M:%S')
    
    st.text("Current:")
    cv_flex = st.container(horizontal=True, horizontal_alignment="center")
    cv_flex.metric("Temperature", f"{latest_df['temperature']:.2f} °C")
    cv_flex.metric("Humidity",    f"{latest_df['humidity']} %")
    cv_flex.metric("Battery", f"{latest_df['battery']:.02f} V")

# Display the amount of data points available
st.text(f"Available data points: {len(df)}", help='This amount may be reduced up to 50% if the selected time frame is >= 1 week.')

# Temperature & Humidity graphs
st.line_chart(df, height=250, x="when", y="temperature", x_label="Date&Time", y_label="Temperature [°C]", color="green")
st.line_chart(df, height=250, x="when", y="humidity"   , x_label="Date&Time", y_label="Humidity [%]")

# Battery graph
st.line_chart(df, height=250, x="when", y="battery", x_label="Date&Time", y_label="Battery [V]", color="yellow")

st.divider()
st.write("_(C) pixelweather 2026_")