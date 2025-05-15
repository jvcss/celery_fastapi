# File C:\work\celery_fastapi\.env
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
# File C:\work\celery_fastapi\docker-compose.yml
services:
  api:
    build: .
    container_name: api
    command: ["api"]
    ports:
      - "8001:8000"
    depends_on:
      - redis

  worker:
    build: .
    container_name: celery_worker
    command: ["worker"]
    depends_on:
      - redis

  beat:
    build: .
    container_name: celery_beat
    command: ["beat"]
    depends_on:
      - redis

  flower:
    build: .
    container_name: celery_flower
    command: ["flower"]
    ports:
      - "5556:5555"
    depends_on:
      - redis

  redis:
    image: redis:7
    container_name: redis
    ports:
      - "6379:6379"
# File C:\work\celery_fastapi\docker-entrypoint.sh
#!/usr/bin/env bash
set -e

case "$1" in
  api)
    exec uvicorn app.main:app \
      --host 0.0.0.0 --port 8000 --workers 2
    ;;
  worker)
    exec celery -A app.celery.app worker \
      --loglevel=info --concurrency=2
    ;;
  beat)
    exec celery -A app.celery.app beat \
      --loglevel=info
    ;;
  flower)
    exec celery -A app.celery.app flower \
      --port=5555 --loglevel=info
    ;;
  *)
    echo "Usage: $0 {api|worker|beat|flower}"
    exit 1
    ;;
esac
# File C:\work\celery_fastapi\app\__init__.py
# File C:\work\celery_fastapi\app\main.py
from fastapi import FastAPI, Body
from .celery.worker import create_task
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})
# File C:\work\celery_fastapi\app\celery\__init__.py
# File C:\work\celery_fastapi\app\celery\app.py
from celery import Celery
from app.core.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    broker_url = CELERY_BROKER_URL,
    result_backend = CELERY_RESULT_BACKEND,
    task_serializer = 'json',
    result_serializer = 'json',
    accept_content = ['json'],
    include=["app.celery.worker"],
    broker_transport_options={
        'max_retries': 1,
        'visibility_timeout': 365*24*60*60,
    }
)
# File C:\work\celery_fastapi\app\celery\worker.py
import os
import time
# from celery import Celery
from .app import celery_app

@celery_app.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
# File C:\work\celery_fastapi\app\core\__init__.py
# File C:\work\celery_fastapi\app\core\config.py
from starlette.config import Config

config = Config(".env")

CELERY_BROKER_URL: str = config("CELERY_BROKER_URL", default="")
CELERY_RESULT_BACKEND: str = config("CELERY_RESULT_BACKEND", default="")
