import requests
import logging
import time
import os
from datetime import datetime, timezone

MAX_RETRIES = 3
BASE_URL = "https://api.football-data.org/v4"
SEASONS = [2024, 2025]
COMPETITION = "PL"
BUCKET = "raw"
SECONDS_BETWEEN_CALLS = 6


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

def get_api_content(url: str, token: str):

    header = {
        'X-Auth-Token': token
    }
    for i in range(1, MAX_RETRIES + 1):
        response = requests.get(url, headers=header, timeout=30)

        if (response.status_code == 200):
            return response.json()
        if (response.status_code == 429):
            waiting_time = int(response.headers.get("Retry-After", 60))
            log.warning("Rate limit atingido, aguardadndo %ds. tentativas(%d/%d)", waiting_time, i, MAX_RETRIES)
            time.sleep(waiting_time)
            continue

        response.raise_for_status();
    raise RuntimeError(f"Falhou apos {MAX_RETRIES}: {url}")
        


def run():
    token = os.environ["FOOTBALL_DATA_API_TOKEN"]
    ingested_at = datetime.now(timezone.utc()).strftime("%Y-%m-%d")

    for season in SEASONS:

        log.info("extraindo a época %d...", season)
        matches = get_api_content(f"{BASE_URL}/competitions/{COMPETITION}/matches?season={season}", token)

    



if __name__ == "__main__":
    run()