import csv
from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.models import Asset


def ingest_csv():
    if SessionLocal is None:
        return {"error": "Database not configured"}

    db: Session = SessionLocal()

    try:
        with open("ingestion/assets.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                asset = (
                    db.query(Asset)
                    .filter(Asset.symbol == row["symbol"])
                    .first()
                )

                if asset:
                    asset.price = float(row["price"])
                    asset.source = row["source"]
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
