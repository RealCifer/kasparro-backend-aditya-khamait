import time
import threading

from services.coinpaprika_ingest import ingest_coinpaprika
from services.coingecko_ingest import ingest_coingecko


def etl_loop(interval_seconds: int = 300):
    """
    Runs ETL periodically in background.
    """
    while True:
        try:
            print("Running scheduled CoinPaprika ETL...")
            ingest_coinpaprika(limit=20)

            print("Running scheduled CoinGecko ETL...")
            ingest_coingecko(limit=20)

            print("ETL cycle completed")
        except Exception as e:
            print("ETL error:", e)

        time.sleep(interval_seconds)


def start_scheduler():
    thread = threading.Thread(
        target=etl_loop,
        daemon=True
    )
    thread.start()
