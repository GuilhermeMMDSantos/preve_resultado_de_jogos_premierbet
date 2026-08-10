import argparse
import os
import psycopg2
import logging
from datetime import datetime, timezone

from minio_client import get_minio_client, read_json, read_bytes



BUCKET = "raw"
SEASON = [2024, 2025]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def read_postgres_password():
    with open(os.environ["POSTGRES_PASSWORD_FILE"]) as f:
        return f.read().strip()


def connect():
    return psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user= os.environ["POSTGRES_USER"],
        password=read_postgres_password()
    )

def ensure_tables(conn):
    with open("./ddl_raw.sql") as f:
        ddl = f.read()
    with conn.cursor() as cur:
        cur.execute(ddl)
    conn.commit()

def load_matches(minio_client, conn, season, ingested_at):
    json_matches = read_json(minio_client, BUCKET, f"/api-football-data/matches/season={season}/ingested_at={ingested_at}/matches.json")
    
  

def run(ingested_at):

    minio_client = get_minio_client()
    conn = connect()

    try:
        ensure_tables(conn)
        for season in SEASON:
            load_matches(minio_client, conn, season, ingested_at)
            break

    finally:
        conn.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ingested-at",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Particao da data Y-m-d a carregar"
    )
    args = parser.parse_args()
    run(ingested_at=args.ingested_at)