from kafka import KafkaConsumer
import json
from cassandra.cluster import Cluster
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# ---------------------------
# Cassandra Connection
# ---------------------------
cluster = Cluster(["127.0.0.1"])
session = cluster.connect()

session.execute("""
CREATE KEYSPACE IF NOT EXISTS substation
WITH replication = {'class':'SimpleStrategy','replication_factor':1};
""")

session.set_keyspace("substation")

session.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id UUID PRIMARY KEY,
    temperature float,
    humidity float,
    vibration float,
    voltage float,
    anomaly boolean
);
""")

# ---------------------------
# Load / Train ML Model
# ---------------------------
try:
    model = joblib.load("model.pkl")
except:
    data = np.random.rand(500,4)
    model = IsolationForest(contamination=0.05)
    model.fit(data)
    joblib.dump(model,"model.pkl")

# ---------------------------
# Kafka Consumer
# ---------------------------
consumer = KafkaConsumer(
    "sensor-topic",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Consumer running...")

for msg in consumer:
    d = msg.value

    X = [[d["temperature"], d["humidity"], d["vibration"], d["voltage"]]]
    pred = model.predict(X)[0]

    anomaly = True if pred == -1 else False

    session.execute("""
        INSERT INTO sensor_data (id, temperature, humidity, vibration, voltage, anomaly)
        VALUES (uuid(), %s, %s, %s, %s, %s)
    """, (d["temperature"], d["humidity"], d["vibration"], d["voltage"], anomaly))

    print("Stored:", d, "Anomaly:", anomaly)