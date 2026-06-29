# IoT Environmental Monitoring System

An IoT environmental monitoring system that simulates sensors and monitors temperature, humidity, and air quality in five locations.

## What the Project Does

* Simulates five IoT environmental sensors:

  * Room 1
  * Room 2
  * Room 3
  * Kitchen
  * Laboratory
* Publishes temperature, humidity, and air-quality readings through MQTT.
* Receives and processes messages using a Python subscriber.
* Stores the same readings in MySQL, MongoDB, and Neo4j.
* Detects abnormal environmental values, such as high temperature, high humidity, and poor air quality.
* Displays current readings, alerts, historical measurements, and a temperature trend chart in a Streamlit dashboard.

## Technologies Used

* Python
* MQTT
* Eclipse Mosquitto
* Paho MQTT
* Docker and Docker Compose
* MySQL
* MongoDB
* Neo4j
* Streamlit
* Pandas

## System Architecture

```text
Simulated Sensors
        ↓
Python Publisher
        ↓
MQTT Broker (Mosquitto)
        ↓
Python Subscriber
        ↓
MySQL + MongoDB + Neo4j
        ↓
Streamlit Dashboard
```

## Project Files

```text
docker-compose.yml              Docker configuration for all services
mosquitto/config/mosquitto.conf Mosquitto broker configuration
publisher.py                    Simulates sensors and publishes MQTT messages
subscriber.py                   Receives MQTT messages and stores data
dashboard.py                    Streamlit monitoring dashboard
requirements.txt                Required Python libraries
```

## How to Run the Project

### 1. Install Python packages

```bash
python3 -m pip install -r requirements.txt
```

### 2. Start Docker services

Make sure Docker Desktop is running, then run:

```bash
docker compose up -d
```

This starts:

* Mosquitto MQTT broker
* MySQL
* MongoDB
* Neo4j

To verify that the containers are running:

```bash
docker ps
```

### 3. Start the subscriber

Open a terminal inside the project folder:

```bash
python3 subscriber.py
```

The subscriber listens to the MQTT topic:

```text
iot/environment
```

It receives readings and saves them in MySQL, MongoDB, and Neo4j.

### 4. Start the publisher

Open another terminal:

```bash
python3 publisher.py
```

The publisher generates simulated readings every few seconds.

### 5. Start the dashboard

Open another terminal:

```bash
python3 -m streamlit run dashboard.py
```

Open the local address shown in the terminal, usually:

```text
http://localhost:8501
```

## Database Verification

### MySQL

```bash
docker exec -it mysql-db mysql -u root -proot iot_project
```

```sql
SELECT * FROM measurements ORDER BY id DESC LIMIT 10;
```

### MongoDB

```bash
docker exec -it mongo-db mongosh
```

```javascript
use iot_project
db.measurements.find().sort({ _id: -1 }).limit(10)
```

### Neo4j

Open:

```text
http://localhost:7474
```

Login:

```text
Username: neo4j
Password: password123
```

Example queries:

```cypher
MATCH (s:Sensor)-[r:LOCATED_IN]->(l:Location)
RETURN s, r, l
```

```cypher
MATCH (s:Sensor)-[r:RECORDED]->(m:Measurement)
WITH s, collect(m)[0] AS m, collect(r)[0] AS r
RETURN s, r, m
```

## Alert Rules

| Condition               | Alert                 |
| ----------------------- | --------------------- |
| Temperature above 40 °C | Very high temperature |
| Temperature above 30 °C | High temperature      |
| Humidity above 70%      | High humidity         |
| Air quality below 50    | Poor air quality      |

## Author

Siham Sadik
