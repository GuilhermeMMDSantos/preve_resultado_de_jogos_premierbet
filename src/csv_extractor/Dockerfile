FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY extract_football_data_csv.py minio_client.py ./

CMD ["python", "extract_football_data_csv.py"]