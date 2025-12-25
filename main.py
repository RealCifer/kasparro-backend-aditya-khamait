from fastapi import FastAPI, Query, HTTPException
from typing import List
import time
import uuid

from schemas.asset import AssetResponse
from services.coinpaprika_ingest import ingest_coinpaprika
from services.coingecko_ingest import ingest_coingecko
from services.asset_service import get_assets
from ingestion.csv_ingest import ingest_csv  

app = FastAPI(title="Kasparro Backend & ETL System")


@app.on_event("startup")
def startup_event():
    """
    Startup logic:
    - Try DB init
    - If DB available → start scheduler
    - If DB unavailable → API still runs (Render-safe)
    """
    try:
        from core.init_db import init_db
        from services.scheduler import start_scheduler

        init_db()
        start_scheduler()
        print("Database connected & scheduler started")

    except Exception as e:
        print("Database not available, running API-only mode")
        print(e)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "scheduler": "enabled if DB available",
        "etl": "runs every 15 minutes when scheduler is active"
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


@app.post("/ingest/csv")
def ingest_csv_endpoint():
    """
    Ingest assets from CSV file
    """
    return ingest_csv()

@app.get("/assets", response_model=List[AssetResponse])
def read_assets(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    try:
        from core.db import SessionLocal
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database not configured"
        )

    if SessionLocal is None:
        raise HTTPException(
            status_code=503,
            detail="Database not configured"
        )

    db = SessionLocal()
    try:
        return get_assets(db, limit, offset)
    finally:
        db.close()
