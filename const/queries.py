# Select Node IDs.
SELECT_NODES = "SELECT id AS node_id FROM devices;"

# Select Node measurements with time cutoff
SELECT_MEASUREMENTS = \
'SELECT temperature, humidity, air_pressure, battery, "when" FROM measurements' \
' WHERE node = :node AND "when" >= :cutoff' \
' ORDER BY "when" ASC;'

SELECT_LATEST_DEW_POINTS = "SELECT \"when\", pwmp_calc_dew_point (temperature, humidity) AS dew_point, pwmp_categorize_dew_point (pwmp_calc_dew_point (temperature, humidity)) AS dew_point_rating FROM measurements WHERE node = :node ORDER BY \"when\" DESC LIMIT 2;"

SELECT_NODE_RUNTIME = "SELECT diff_interval::TEXT FROM pwmp_get_node_total_runtime(:node);"