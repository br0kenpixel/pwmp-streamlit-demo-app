import streamlit as st

st.title("PixelWeather Demo Dashboard")
st.write(
    "Note that this app is for demonstration purposes only! _Thanks for checking out anyway!_"
)

# PG coonection
conn = st.connection("pwmp-db", type="sql")

# Node Selector
nodes = conn.query("SELECT id AS node_id FROM devices;")
selected_node = st.selectbox("Node", nodes, help="Pick a node")

# Temperature & Humidity graphs
df = conn.query('SELECT temperature, humidity, "when" FROM measurements WHERE node = :node ORDER BY "when" DESC LIMIT 100;', ttl="10m", params={"node": selected_node})
st.write(f"Available data points: {len(df)}")
st.line_chart(df, height=250, x="when", y="temperature", x_label="Date&Time", y_label="Temperature [°C]", color="green")
st.line_chart(df, height=250, x="when", y="humidity"   , x_label="Date&Time", y_label="Humidity [%]")

st.divider()
st.write("_(C) pixelweather 2026_")