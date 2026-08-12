import argparse
import os
import psycopg2
import psycopg2.extras
import logging
from datetime import datetime, timezone
import json

from minio_client import get_minio_client, read_json, read_bytes

from queries import UPSERT_MATCHES, UPSERT_TEAMS

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
    key = f"/api-football-data/matches/season={season}/ingested_at={ingested_at}/matches.json"
    data = read_json(minio_client, BUCKET, key)
    rows = []
    for m in data.get("matches", []):
        score = m.get("score", {}) or {}
        full_time = score.get("fullTime", {}) or {}
        rows.append((
            m["id"],
            season,
            m.get("matchday"),
            m.get("utcDate"),
            m.get("status"),
            (m.get("homeTeam") or {}).get("id"),
            (m.get("homeTeam") or {}).get("name"),
            (m.get("awayTeam") or {}).get("id"),
            (m.get("awayTeam") or {}).get("name"),
            full_time.get("home"),
            full_time.get("away"),
            score.get("winner"),
            json.dumps(m),
            ingested_at
        ))
    with conn.cursor() as cur:
        psycopg2.extras.execute_values(cur, UPSERT_MATCHES, rows)
    conn.commit()
    logger.info("raw.matches: %d linhas (season: %d)", len(rows), season)

def load_teams(minio_client, conn, season, ingested_at):
    key = f"/api-football-data/times/season={season}/ingested_at={ingested_at}/times.json"
    data = read_json(minio_client, BUCKET, key)
    rows = []
    for t in data.get("teams", {}):
        rows.append((
            t["id"],
            season,
            t["name"],
            t.get("shortName"),
            t.get("tla"),
            json.dumps(t),
            ingested_at
        ))
    with conn.cursor() as cur:
        psycopg2.extras.execute_values(cur, UPSERT_TEAMS, rows)
    conn.commit()
    logger.info("raw.teams: %d linhas (season: %d)", len(rows), season)

  

def run(ingested_at):

    minio_client = get_minio_client()
    conn = connect()

    try:
        ensure_tables(conn)
        for season in SEASON:
            load_matches(minio_client, conn, season, ingested_at)
            load_teams(minio_client, conn, season, ingested_at)
    finally:
        conn.close()
    logger.info("load completa")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ingested-at",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Particao da data Y-m-d a carregar"
    )
    args = parser.parse_args()
    run(ingested_at=args.ingested_at)