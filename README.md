# Real-time-Substation-Condition-Monitoring-System-for-Predictive-Maintenance-in-Power-Grids 


Steps to build this project locally

```
cd to the project folder
docker compose up -d
```

Install Python Requirements!

```
pip install -r requirements.txt
```

Run Producer Server

Inside services folder run:
```
uvicorn producer_gateway:app --reload
```

Server starts at:

http://127.0.0.1:8000

run:
```
python consumer_engine.py
```
If working correctly, you’ll see:

Consumer running...