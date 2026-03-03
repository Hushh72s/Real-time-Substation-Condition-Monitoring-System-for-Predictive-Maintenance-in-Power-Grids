from fastapi import FastAPI
from cassandra.cluster import Cluster
import time

app = FastAPI()

# Retry loop for Cassandra connection
connected = False
while not connected:
    try:
        cluster = Cluster(["127.0.0.1"])
        session = cluster.connect("substation")
        connected = True
        print("Connected to Cassandra")
    except:
        print("Waiting for Cassandra...")
        time.sleep(5)

@app.get("/latest")
def latest():
    rows = session.execute("""
        SELECT * FROM sensor_data
        LIMIT 1
    """)
    for r in rows:
        return dict(r._asdict())
    return {"msg":"no data"}

@app.get("/history")
def history():
    rows = session.execute("""
        SELECT * FROM sensor_data
        LIMIT 50
    """)
    return [dict(r._asdict()) for r in rows]

@app.get("/status")
def status():
    rows = session.execute("""
        SELECT anomaly FROM sensor_data
        LIMIT 1
    """)
    for r in rows:
        return {"anomaly": r.anomaly}
    return {"msg":"no data"}