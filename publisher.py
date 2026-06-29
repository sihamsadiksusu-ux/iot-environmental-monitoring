import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
topic = "iot/environment"

client = mqtt.Client()
client.connect(broker, port)

sensors = [
    {
        "sensor_id": "S1",
        "location": "Room 1",
        "normal_temperature": (21, 27),
        "normal_humidity": (40, 60),
        "normal_air_quality": (70, 100)
    },
    {
        "sensor_id": "S2",
        "location": "Room 2",
        "normal_temperature": (21, 28),
        "normal_humidity": (40, 65),
        "normal_air_quality": (65, 100)
    },
    {
        "sensor_id": "S3",
        "location": "Room 3",
        "normal_temperature": (20, 27),
        "normal_humidity": (38, 62),
        "normal_air_quality": (70, 100)
    },
    {
        "sensor_id": "S4",
        "location": "Kitchen",
        "normal_temperature": (23, 30),
        "normal_humidity": (45, 68),
        "normal_air_quality": (55, 95)
    },
    {
        "sensor_id": "S5",
        "location": "Laboratory",
        "normal_temperature": (21, 28),
        "normal_humidity": (35, 60),
        "normal_air_quality": (50, 95)
    }
]

while True:
    sensor = random.choice(sensors)

    temperature = round(random.uniform(*sensor["normal_temperature"]), 2)
    humidity = round(random.uniform(*sensor["normal_humidity"]), 2)
    air_quality = round(random.uniform(*sensor["normal_air_quality"]), 2)

    event = random.random()

    if event < 0.10:
        temperature = round(random.uniform(41, 55), 2)
    elif event < 0.25:
        temperature = round(random.uniform(31, 40), 2)
    elif event < 0.35:
        humidity = round(random.uniform(71, 85), 2)
    elif event < 0.45:
        air_quality = round(random.uniform(30, 49), 2)

    data = {
        "sensor_id": sensor["sensor_id"],
        "location": sensor["location"],
        "temperature": temperature,
        "humidity": humidity,
        "air_quality": air_quality,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    message = json.dumps(data)
    client.publish(topic, message)

    print("Published:", message)

    time.sleep(3)