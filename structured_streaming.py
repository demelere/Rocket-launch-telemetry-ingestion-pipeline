from pyspark.sql.functions import from_json, window
from influxdb import InfluxDBClient

influxdb_host = 'localhost'
influxdb_port = 8086
influxdb_user = 'admin'
influxdb_pass = 'admin'
influxdb_db = 'telemetry_data'

influxdb_client = InfluxDBClient(host=influxdb_host, port=influxdb_port, username=influxdb_user, password=influxdb_pass)
influxdb_client.create_database(influxdb_db)

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor_data") \
    .load()

schema = "time timestamp, altitude double, speed double"
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

agg_df = parsed_df \
    .withWatermark("time", "10 minutes") \
    .groupBy(window("time", "1 minute")) \
    .agg({"altitude": "avg", "speed": "avg"}) \
    .select("window.start", "window.end", "avg(altitude)", "avg(speed)")

query = agg_df \
    .writeStream \
    .queryName("sensor_data_query") \
    .outputMode("append") \
    .format("console") \
    .foreachBatch(lambda batch_df, batch_id: batch_df.toPandas().apply(
        lambda row: influxdb_client.write_points([{
            "measurement": "telemetry_metrics",
            "tags": {
                "metric": "rocket_launch_metrics"
            },
            "time": row["window.start"].strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fields": {
                "altitude": row["avg(altitude)"],
                "speed": row["avg(speed)"]
            }
        }]), axis=1)) \
    .start()
