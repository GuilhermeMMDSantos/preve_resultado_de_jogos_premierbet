import requests
import logging
from minio_client import get_minio_client, ensure_bucket_exists, upload_csv
from datetime import datetime, timezone
import time

BASE_URL = "https://www.football-data.co.uk/mmz4281"
SEASONS = [2425, 2526]
BUCKET = "raw"
DIVISION = "E0" #para premier league

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def run():
   
    minio_client = get_minio_client()
    ingested_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ensure_bucket_exists(minio_client, BUCKET)

    for season in SEASONS:
        logger.info("extraindo csv da temporada %d...", season)
        url = f"{BASE_URL}/{season}/{DIVISION}.csv"
        data = requests.get(url, timeout=30)
        data.raise_for_status()
        key = f"football-data-csv/season={season}/ingested_at={ingested_at}/{DIVISION}.csv"
        upload_csv(minio_client, BUCKET, key, data.content, content_type="text/csv")
        time.sleep(6)

    logger.info("extração concluída")

if __name__ == "__main__":
    run()