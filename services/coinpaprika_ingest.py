import requests
from datetime import datetime
from sqlalchemy.orm import Session

from core.db import SessionLocal
from core.models import RawCoinPaprika, Asset
from core.retry import retry  

BASE_URL = "https://api.coinpaprika.com/v1"


def fetch_tickers(limit: int = 50):
    def _call():
        url = f"{BASE_URL}/tickers"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()[:limit]

    return retry(_call, retries=3, delay_seconds=2)


def ingest_coinpaprika(limit: int = 50):
    db: Session = SessionLocal()
    try:
        coins = fetch_tickers(limit)

        for coin in coins:
            price = coin["quotes"]["USD"]["price"]

            raw = RawCoinPaprika(
                symbol=coin["symbol"],
                name=coin["name"],
                price=price,
                fetched_at=datetime.utcnow(),
            )
            db.add(raw)

            asset = (
                db.query(Asset)
                .filter(Asset.symbol == coin["symbol"])
                .first()
            )

            if asset:
                asset.price = price
                asset.updated_at = datetime.utcnow()
                asset.source = "coinpaprika"
            else:
                asset = Asset(
                    symbol=coin["symbol"],
                    name=coin["name"],
                    price=price,
                    source="coinpaprika",
                )
                db.add(asset)

        db.commit()
        return {"ingested": len(coins)}

    except Exception as e:
        db.rollback()
        print("CoinPaprika ETL failed:", e)
        raise
    finally:
        db.close()
