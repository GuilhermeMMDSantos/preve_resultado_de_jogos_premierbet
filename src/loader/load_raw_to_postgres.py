import argparse
import os
import psycopg2
import psycopg2.extras
import logging
from datetime import datetime, timezone
import json
import pandas as pd
import io

from minio_client import get_minio_client, read_json, read_bytes

from queries import UPSERT_MATCHES, UPSERT_TEAMS, UPSERT_CSV_MATCHES

BUCKET = "raw"
SEASON = [2024, 2025]
SEASON_CODE = [2425, 2526]
DIVISION = "E0"

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

def load_matches_csv(minio_client, conn, season, ingested_at):
    key = f"football-data-csv/season={season}/ingested_at={ingested_at}/{DIVISION}.csv"
    data_bytes = read_bytes(minio_client, BUCKET, key)
    df = pd.read_csv(io.BytesIO(data_bytes))
    df = df.dropna(subset=["Date", "HomeTeam", "AwayTeam"])
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    rows = []
    for _,r in df.iterrows():
        r_dict = r.where(pd.notnull(r), None).to_dict()
        r_dict["Date"] = r_dict["Date"].strftime("%Y-%m-%d")
        rows.append((
            season,
            r["Date"].date(),
            r["HomeTeam"],
            r["AwayTeam"],
            r.get("FTHG"),
            r.get("FTAG"),
            r.get("FTR"),
            json.dumps(r_dict),
            ingested_at
        ))

    with conn.cursor() as cur:
        psycopg2.extras.execute_values(cur, UPSERT_CSV_MATCHES, rows)
    conn.commit()
    logger.info("raw.matches_csv: %d linhas (season %d) ", len(rows), season)



def run(ingested_at):

    minio_client = get_minio_client()
    conn = connect()

    try:
        ensure_tables(conn)
        for season in SEASON:
            load_matches(minio_client, conn, season, ingested_at)
            load_teams(minio_client, conn, season, ingested_at)
        for season_code in SEASON_CODE:
            load_matches_csv(minio_client, conn, season_code, ingested_at)
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