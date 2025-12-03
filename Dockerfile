
# ------------ Stage 1: Builder ------------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# ------------ Stage 2: Runtime ------------
FROM python:3.11-slim

ENV TZ=UTC

WORKDIR /app

RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
 && rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

RUN chmod 0644 /app/cron/log_2fa
RUN crontab /app/cron/log_2fa

RUN mkdir -p /data /cron && chmod 755 /data /cron

EXPOSE 8080

CMD service cron start && uvicorn app:app --host 0.0.0.0 --port 8080
