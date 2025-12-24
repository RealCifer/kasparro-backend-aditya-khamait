from apscheduler.schedulers.background import BackgroundScheduler
from services.coinpaprika_ingest import ingest_coinpaprika
from services.coingecko_ingest import ingest_coingecko

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        func=ingest_coinpaprika,
        trigger="interval",
        minutes=15,
        id="coinpaprika_etl"
    )

    scheduler.add_job(
        func=ingest_coingecko,
        trigger="interval",
        minutes=15,
        id="coingecko_etl"
    )

    scheduler.start()
    return scheduler
