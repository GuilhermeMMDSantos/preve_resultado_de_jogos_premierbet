import argparse
import os
import psycopg2
from datetime import datetime, timezone

from load_raw_to_postgres import get_minio_client, read_json, read_bytes

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


def run(args):

    minio_client = get_minio_client()
    conn = connect()

    try:
        ensure_tables(conn)
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
    run(args=args.ingested_at)