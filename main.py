from fastapi import FastAPI
from services.coinpaprika_ingest import ingest_coinpaprika

import time
import uuid
import time as t

from sqlalchemy.exc import OperationalError
from core.init_db import init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    retries = 10
    while retries > 0:
        try:
            init_db()
            print("Database connected and tables ready")
            break
        except OperationalError:
            retries -= 1
            print("Waiting for database to be ready...")
            t.sleep(3)

    if retries == 0:
        raise Exception("Database not ready after retries")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "db": "connected",
        "last_etl_run": "pending"
    }

@app.get("/data")
def get_data(limit: int = 10, offset: int = 0):
    start = time.time()
    return {
        "request_id": str(uuid.uuid4()),
        "api_latency_ms": int((time.time() - start) * 1000),
        "data": []
    }

@app.post("/ingest/coinpaprika")
def ingest(limit: int = 50):
    return ingest_coinpaprika(limit)
