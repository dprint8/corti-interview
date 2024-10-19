# producer/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY producer.py ./
COPY input.txt /data/input.txt

CMD ["python", "producer.py"]
