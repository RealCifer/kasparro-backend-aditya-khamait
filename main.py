from fastapi import FastAPI
import time
import uuid

app = FastAPI()

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
