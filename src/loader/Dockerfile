FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY minio_client.py load_raw_to_postgres.py ddl_raw.sql ./

CMD ["python", "load_raw_to_postgres.py"]