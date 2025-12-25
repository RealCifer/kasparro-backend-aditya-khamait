import csv
from pathlib import Path
from core.db import SessionLocal
from core.models import Asset


def ingest_csv():
    file_path = Path(__file__).parent / "assets.csv"

    if not file_path.exists():
        return {"status": "CSV file not found"}

    db = SessionLocal()
    try:
        with open(file_path, newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                asset = Asset(
                    symbol=row["symbol"],
                    name=row["name"],
                    price=float(row["price"]),
                    source=row["source"]
                )
                db.merge(asset)

            db.commit()

        return {"status": "CSV ingestion completed"}

    finally:
        db.close()
