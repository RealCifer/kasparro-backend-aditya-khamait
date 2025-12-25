import csv
import os
from core.db import SessionLocal
from core.models import Asset


def ingest_csv():
    try:
        db = SessionLocal()
    except Exception:
        return {"error": "Database not configured"}

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(BASE_DIR, "assets.csv")

        if not os.path.exists(csv_path):
            return {"error": "assets.csv not found"}

        with open(csv_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

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

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()
