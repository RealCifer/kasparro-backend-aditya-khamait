import csv
from pathlib import Path
from sqlalchemy.exc import IntegrityError
from core.db import SessionLocal
from core.models import CSVAsset


CSV_PATH = Path("ingestion/assets.csv")


def ingest_csv():
    if not CSV_PATH.exists():
        return {"error": "CSV file not found"}

    db = SessionLocal()
    inserted = 0

    with open(CSV_PATH, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                asset = CSVAsset(
                    symbol=row["symbol"],
                    name=row["name"],
                    price=float(row["price"]),
                    source=row.get("source", "csv")
                )
                db.add(asset)
                db.commit()
                inserted += 1
            except IntegrityError:
                db.rollback()  

    db.close()

    return {
        "status": "CSV ingestion completed",
        "inserted": inserted
    }
