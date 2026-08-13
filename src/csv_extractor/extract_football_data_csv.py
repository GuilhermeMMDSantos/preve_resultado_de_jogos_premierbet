import requests
import logging
from minio_client import get_minio_client, ensure_bucket_exists, upload_csv
from datetime import datetime, timezone
import time

SEASONS = [2425, 2526]
BUCKET = "raw"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def run():
    BASE_URL = "https://www.football-data.co.uk/englandm/mmz4281"
    minio_client = get_minio_client()
    ingested_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for season in SEASONS:
        logger.info("extraindo csv da temporada %d...", season)
        data = requests.get(f"{BASE_URL}/{season}/E0.csv", timeout=10)
        if requests.status_codes != 200:
            data.raise_for_status()
        ensure_bucket_exists(minio_client, BUCKET)
        upload_csv(minio_client, BUCKET, f"football-data/season={season}/ingested_at={ingested_at}/E0.csv")
        time.sleep(6)

    logger.info("extração concluída")

if __name__ == "__main__":
    run()