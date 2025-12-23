from fastapi import FastAPI, Query
from typing import List

import time
import uuid
import time as t

from sqlalchemy.exc import OperationalError

from core.init_db import init_db
from core.db import SessionLocal

from services.coinpaprika_ingest import ingest_coinpaprika
from services.coingecko_ingest import ingest_coingecko
from services.asset_service import get_assets
from services.scheduler import start_scheduler

from schemas.asset import AssetResponse


app = FastAPI(title="Kasparro Backend & ETL System")


@app.on_event("startup")
def startup_event():
    db_connected = False

    try:
        init_db()
        db_connected = True
        print("Database connected and tables ready")
    except Exception as e:
        print("Database not available, starting API without DB:", e)

    if db_connected:
        try:
            start_scheduler()
            print("ETL scheduler started")
        except Exception as e:
            print("Scheduler failed to start:", e)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "db": "connected (or optional)",
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
def ingest_coinpaprika_endpoint(
    limit: int = Query(50, ge=1, le=100)
):
    return ingest_coinpaprika(limit)


@app.post("/ingest/coingecko")
def ingest_coingecko_endpoint(
    limit: int = Query(50, ge=1, le=100)
):
    return ingest_coingecko(limit)


@app.get("/assets", response_model=List[AssetResponse])
def read_assets(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    db = SessionLocal()
    try:
        return get_assets(db, limit, offset)
    finally:
        db.close()
