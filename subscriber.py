import json
import time
import paho.mqtt.client as mqtt
import mysql.connector
from pymongo import MongoClient
from neo4j import GraphDatabase

mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="iot_project"
)

mysql_cursor = mysql_db.cursor()

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["iot_project"]
mongo_collection = mongo_db["measurements"]

neo4j_driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password123")
)

def save_to_mysql(data):
    sql = """
    INSERT INTO measurements
    (sensor_id, location, temperature, humidity, air_quality, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        data["sensor_id"],
        data["location"],
        data["temperature"],
        data["humidity"],
        data["air_quality"],
        data["timestamp"]
    )

    mysql_cursor.execute(sql, values)
    mysql_db.commit()

def save_to_mongodb(data):
    mongo_collection.insert_one(data.copy())

def save_to_neo4j(data):
    query = """
    MERGE (s:Sensor {id: $sensor_id})
    MERGE (l:Location {name: $location})
    CREATE (m:Measurement {
        temperature: $temperature,
        humidity: $humidity,
        air_quality: $air_quality,
        timestamp: $timestamp
    })
    MERGE (s)-[:LOCATED_IN]->(l)
    CREATE (s)-[:RECORDED]->(m)
    """

    with neo4j_driver.session() as session:
        session.run(query, **data)

message_count = 0
total_processing_time = 0

def on_message(client, userdata, message):
    global message_count, total_processing_time

    start_time = time.perf_counter()

    data = json.loads(message.payload.decode())

    print("Received:", data)

    save_to_mysql(data)
    save_to_mongodb(data)
    save_to_neo4j(data)

    end_time = time.perf_counter()

    processing_time = end_time - start_time

    message_count += 1
    total_processing_time += processing_time

    average_time = total_processing_time / message_count

    print("Saved in MySQL, MongoDB, and Neo4j")
    print(f"Message {message_count} processing time: {processing_time:.4f} seconds")
    print(f"Average processing time: {average_time:.4f} seconds")

broker = "localhost"
port = 1883
topic = "iot/environment"

client = mqtt.Client()
client.on_message = on_message

client.connect(broker, port)
client.subscribe(topic)

print("Subscriber is listening...")
client.loop_forever()
