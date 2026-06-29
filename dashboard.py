import streamlit as st
import pandas as pd
import mysql.connector

mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="iot_project"
)

query = """
SELECT id, sensor_id, location, temperature, humidity, air_quality, timestamp
FROM measurements
ORDER BY id DESC
LIMIT 300
"""

df = pd.read_sql(query, mysql_db)

st.title("IoT Environmental Monitoring Dashboard")

st.write("Dashboard for monitoring temperature, humidity, and air quality in five rooms.")

def get_alerts(row):
    alerts = []

    if row["temperature"] > 40:
        alerts.append(f"Very high temperature: {row['temperature']} °C")
    elif row["temperature"] > 30:
        alerts.append(f"High temperature: {row['temperature']} °C")

    if row["humidity"] > 70:
        alerts.append(f"High humidity: {row['humidity']} %")

    if row["air_quality"] < 50:
        alerts.append(f"Poor air quality: {row['air_quality']}")

    return alerts

if df.empty:
    st.info("No data found yet.")
else:
    latest = df.iloc[0]

    st.subheader("Latest Received Reading")

    col1, col2, col3 = st.columns(3)

    col1.metric("Temperature", f"{latest['temperature']} °C")
    col2.metric("Humidity", f"{latest['humidity']} %")
    col3.metric("Air Quality", f"{latest['air_quality']}")

    latest_alerts = get_alerts(latest)

    if latest_alerts:
        st.error(f"ALERT in {latest['location']}: " + ", ".join(latest_alerts))
    else:
        st.success(f"Latest reading is normal in {latest['location']}")

    st.subheader("Current Status of Each Room")

    latest_by_room = df.sort_values("id", ascending=False).drop_duplicates("location")

    status_rows = []

    for _, row in latest_by_room.iterrows():
        alerts = get_alerts(row)

        if alerts:
            status = "ALERT"
            alert_text = ", ".join(alerts)
        else:
            status = "NORMAL"
            alert_text = "No current alert"

        status_rows.append({
            "sensor_id": row["sensor_id"],
            "location": row["location"],
            "temperature": row["temperature"],
            "humidity": row["humidity"],
            "air_quality": row["air_quality"],
            "status": status,
            "alerts": alert_text,
            "timestamp": row["timestamp"]
        })

    status_df = pd.DataFrame(status_rows)

    st.dataframe(status_df)

    st.subheader("Current Room Alerts")

    current_alerts_df = status_df[status_df["status"] == "ALERT"]

    if current_alerts_df.empty:
        st.success("All rooms are currently normal.")
    else:
        st.error("Some rooms currently have abnormal environmental values.")
        st.dataframe(current_alerts_df)

    st.subheader("Historical Measurements")

    st.write("This table keeps old readings, including past alerts, for proof and analysis.")

    st.dataframe(
        df[
            ["id", "sensor_id", "location", "temperature", "humidity", "air_quality", "timestamp"]
        ]
    )

    st.subheader("Temperature Trend")

    chart_data = df.sort_values("id")[["timestamp", "temperature"]]
    chart_data = chart_data.set_index("timestamp")

    st.line_chart(chart_data)