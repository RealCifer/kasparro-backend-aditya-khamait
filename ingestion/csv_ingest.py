import csv
from core.db import SessionLocal
from core.models import Asset


def ingest_csv():
    db = SessionLocal()

    try:
        with open("ingestion/assets.csv", "r") as file:
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
