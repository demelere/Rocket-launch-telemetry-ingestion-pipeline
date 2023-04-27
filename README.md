### Intro
This pipeline processes real-time rocket launch telemetry data using Kafka, PySpark, InfluxDB, and Grafana. The pipeline ingests raw sensor data from a local file, processes the data using PySpark, and stores the results in InfluxDB. The processed data is then visualized using Grafana.

### Running the pipeline
* Install Docker and Docker Compose on your system
* Log in to Docker so that Docker can pull images from Docker Hub
* From the root of the project directory, build the Docker images with `docker-compose build`
* Run the Docker containers using `docker-compose up`
* Connect to Grafana by visiting `http://localhost:3000` in a web browser.
* Use the Kafka producer script to send sensor data to Kafka with `python3 kafka_producer.py`

The pipeline will start ingesting data from the Kafka topic and processing it using PySpark. The processed data will be stored in InfluxDB and visualized in Grafana.

### How the pipeline architecture works
Upon running the project, Docker Compose uses `docker-compose.yml` to start the individual services 

`Dockerfile` uses pip to install the packages (Kafka, PySpark, InfluxDB, Grafana) for the entire pipeline within the container so that the user doesn't have to manually or globally install those on their local machine.  Then it copies over the scripts and runs them.  

`Producer.py` ingests data from a local JSON file with dummy data and publishes it to a Kafka topic.  In a production setting, it would receive and publish live sensor data in place of the dummy data.

`structured-streaming.py` then reads from that Kafka topic, transforms and aggregates rolling averages for every minute, and writes each the data to persist it to InfluxDB.

InfluxDB 