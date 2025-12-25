import csv
from pathlib import Path
from sqlalchemy.orm import Session
from core.models import Asset
from core.db import SessionLocal


CSV_PATH = Path("ingestion/assets.csv")


def ingest_csv():
    if not CSV_PATH.exists():
        return {"error": "CSV file not found"}

    db: Session = SessionLocal()

    try:
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                existing = db.query(Asset).filter_by(symbol=row["symbol"]).first()

                if existing:
                    existing.price = float(row["price"])
                    existing.source = row["source"]
                else:
                    asset = Asset(
                        symbol=row["symbol"],
                        name=row["name"],
                        price=float(row["price"]),
                        source=row["source"],
                    )
                    db.add(asset)

        db.commit()
        return {"status": "CSV ingestion completed"}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()
