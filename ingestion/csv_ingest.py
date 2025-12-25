import csv
import os
from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.models import Asset
from datetime import datetime


CSV_PATH = os.path.join(os.path.dirname(__file__), "assets.csv")


def ingest_csv():
    if not os.path.exists(CSV_PATH):
        return {"error": "CSV file not found"}

    db: Session = SessionLocal()

    try:
        with open(CSV_PATH, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                existing = (
                    db.query(Asset)
                    .filter(Asset.symbol == row["symbol"])
                    .first()
                )

                if existing:
                    # UPDATE
                    existing.name = row["name"]
                    existing.price = float(row["price"])
                    existing.source = row["source"]
                    existing.updated_at = datetime.utcnow()
                else:
                    # INSERT
                    asset = Asset(
                        symbol=row["symbol"],
                        name=row["name"],
                        price=float(row["price"]),
                        source=row["source"],
                        updated_at=datetime.utcnow(),
                    )
                    db.add(asset)

            db.commit()

        return {"status": "CSV ingestion completed"}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()
