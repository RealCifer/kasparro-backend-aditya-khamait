import requests
from datetime import datetime
from sqlalchemy.orm import Session

from core.db import SessionLocal
from core.models import RawCoinPaprika, Asset
from core.retry import retry   # ✅ NEW

BASE_URL = "https://api.coingecko.com/api/v3"


def fetch_markets(limit: int = 50):
    def _call():
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

    return retry(_call, retries=3, delay_seconds=2)


def ingest_coingecko(limit: int = 50):
    db: Session = SessionLocal()
    try:
        coins = fetch_markets(limit)

        for coin in coins:
            price = coin["current_price"]

            raw = RawCoinPaprika(
                symbol=coin["symbol"].upper(),
                name=coin["name"],
                price=price,
                fetched_at=datetime.utcnow(),
            )
            db.add(raw)

            asset = (
                db.query(Asset)
                .filter(Asset.symbol == coin["symbol"].upper())
                .first()
            )

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

    except Exception as e:
        db.rollback()
        print("CoinGecko ETL failed:", e)
        raise
    finally:
        db.close()
