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
nodes = conn.query(SELECT_NODES, ttl=60)
flex = st.container(horizontal=True, horizontal_alignment="right")
selected_node = flex.selectbox("Node", nodes, help="Pick a node")
time_frame = flex.selectbox("Time frame", SELECTABLE_TIME_FRAMES.keys(), help="Pick a time frame")

if selected_node not in nodes["node_id"]:
    st.error("Invalid node selected")
    st.stop()

# Query data
cutoff = datetime.now(timezone.utc) - SELECTABLE_TIME_FRAMES[time_frame]
df = conn.query(SELECT_MEASUREMENTS, ttl="10m", params={"node": selected_node, "cutoff": cutoff})

if df.empty:
    st.warning("No data available for the selected node.")
    st.stop()

# Current values
with st.container(border=True):
    latest_df = df.iloc[-1]
    pre_latest_df = df.iloc[-2]
    
    raw_temperature_delta = latest_df['temperature'] - pre_latest_df['temperature']
    raw_humidity_delta = latest_df['humidity'] - pre_latest_df['humidity']
    raw_pressure_delta = latest_df['air_pressure'] - pre_latest_df['air_pressure']
    raw_battery_delta = latest_df['battery'] - pre_latest_df['battery']

    temperature_delta = f"{raw_temperature_delta:.02f} °C" if raw_temperature_delta != 0 else None
    humidity_delta = f"{raw_humidity_delta} %" if raw_humidity_delta != 0 else None
    air_pressure_delta = f"{raw_pressure_delta} hPa" if raw_pressure_delta != 0 else None
    battery_delta = f"{raw_battery_delta:.02f} V" if abs(round(raw_battery_delta, 2)) != 0 else None

    st.text("Current metrics:")
    cv_flex = st.container(horizontal=True, horizontal_alignment="center")
    cv_flex.metric("Temperature", f"{latest_df['temperature']:.2f} °C", delta=temperature_delta)
    cv_flex.metric("Humidity", f"{latest_df['humidity']} %", delta=humidity_delta)
    cv_flex.metric("Air Pressure", f"{latest_df['air_pressure']} hPa", delta=air_pressure_delta)
    cv_flex.metric("Battery", f"{latest_df['battery']:.02f} V", delta=battery_delta)

# Current report
with st.container(border=True):
    dew_point_stats = conn.query(SELECT_LATEST_DEW_POINTS, ttl=60, params={"node": selected_node})
    runtime_stats = conn.query(SELECT_NODE_RUNTIME, ttl=60, params={"node": selected_node})
    current = dew_point_stats.iloc[0]
    previous = dew_point_stats.iloc[1]

    runtime = runtime_stats["diff_interval"].iloc[0]
    runtime = runtime[0:runtime.find(".")]

    dew_point = current['dew_point']
    raw_dew_point_delta = dew_point - previous['dew_point']
    dew_point_delta = f"{raw_dew_point_delta:.02f} °C" if raw_dew_point_delta != 0 else None

    st.text("Current stats:")
    cs_flex = st.container(horizontal=True, horizontal_alignment="center")
    cs_flex.metric("Dew Point", f"{dew_point:.02f} °C", delta=dew_point_delta)
    cs_flex.metric("Dew Point Rating", current['dew_point_rating'])
    cs_flex.metric("Total runtime", runtime)

if len(df) < 10:
    st.warning("Not enough data points available for graphs")
    st.stop()

# Cut the data frames in half
if SELECTABLE_TIME_FRAMES[time_frame].days >= 7:
    df = df.iloc[::4]

# Display the amount of data points available
st.text(f"Available data points: {len(df)}", help='This amount may be reduced up to 25% if the selected time frame is >= 1 week.')

# Temperature & Humidity graphs
st.line_chart(df, height=250, x="when", y="temperature", x_label="Date&Time", y_label="Temperature [°C]", color="green")
st.line_chart(df, height=250, x="when", y="humidity"   , x_label="Date&Time", y_label="Humidity [%]", color="blue")
st.line_chart(df, height=250, x="when", y="air_pressure"   , x_label="Date&Time", y_label="Air Pressure [hPa]", color="orange")

# Battery graph
st.line_chart(df, height=250, x="when", y="battery", x_label="Date&Time", y_label="Battery [V]", color="yellow")

st.divider()
st.write("_(C) pixelweather 2026_")