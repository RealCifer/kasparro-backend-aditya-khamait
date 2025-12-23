import requests
from datetime import datetime
from sqlalchemy.orm import Session

from core.db import SessionLocal
from core.models import RawCoinPaprika, Asset

BASE_URL = "https://api.coingecko.com/api/v3"


def fetch_markets(limit: int = 50):
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def ingest_coingecko(limit: int = 50):
    db: Session = SessionLocal()
    try:
        coins = fetch_markets(limit)

        for coin in coins:
            price = coin["current_price"]

            # Store RAW (reuse raw table for simplicity)
            raw = RawCoinPaprika(
                symbol=coin["symbol"].upper(),
                name=coin["name"],
                price=price,
                fetched_at=datetime.utcnow(),
            )
            db.add(raw)

            # UPSERT into assets
            asset = db.query(Asset).filter(
                Asset.symbol == coin["symbol"].upper()
            ).first()

            if asset:
                asset.price = price
                asset.updated_at = datetime.utcnow()
                asset.source = "coingecko"
            else:
                asset = Asset(
                    symbol=coin["symbol"].upper(),
                    name=coin["name"],
                    price=price,
                    source="coingecko",
                )
                db.add(asset)

        db.commit()
        return {"ingested": len(coins)}

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
