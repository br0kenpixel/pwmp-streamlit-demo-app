# Select Node IDs.
SELECT_NODES = "SELECT id AS node_id FROM devices;"

# Select Node measurements with time cutoff
SELECT_MEASUREMENTS = \
'SELECT temperature, humidity, battery, "when" FROM measurements' \
' LEFT JOIN statistics ON statistics.measurement = measurements.id' \
' WHERE node = :node AND "when" >= :cutoff' \
' ORDER BY "when" ASC' \
' LIMIT 2000;'