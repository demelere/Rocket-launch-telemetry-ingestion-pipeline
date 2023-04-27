FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y python3 python3-pip wget gnupg2 \
    && pip3 install kafka-python pyspark influxdb

RUN wget -qO- https://repos.influxdata.com/influxdb2.key | apt-key add -
RUN echo "deb https://repos.influxdata.com/ubuntu focal stable" | tee /etc/apt/sources.list.d/influxdb.list
RUN apt-get update && apt-get install -y influxdb

RUN wget -qO- https://packages.grafana.com/gpg.key | apt-key add -
RUN echo "deb https://packages.grafana.com/oss/deb stable main" | tee /etc/apt/sources.list.d/grafana.list
RUN apt-get update && apt-get install -y grafana

COPY ./kafka_producer.py /
COPY ./structured_streaming.py /

EXPOSE 8086
EXPOSE 3000

CMD influxd & \
    service grafana-server start & \
    python3 kafka_producer.py & \
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 structured_streaming.py
