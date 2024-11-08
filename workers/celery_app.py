import logging
import os
from datetime import timedelta

from celery import Celery
from dotenv import load_dotenv

from db.utils import DatabaseSession
from services.setup_logging import setup_logging

load_dotenv()

setup_logging()
logger = logging.getLogger(__name__)

RELOAD_TIMEOUT_SECONDS: int = int(os.getenv("RELOAD_TIMEOUT_SECONDS", 60))
REDIS_URI: str = os.getenv("REDIS_URI", "redis://localhost:6379/0")
DB_PATH: str = os.getenv("DB_PATH")
TELEGRAM_ID_WHITE_LIST: list[str | int] = os.getenv("TELEGRAM_ID_WHITE_LIST", "").split(",")

session = DatabaseSession(DB_PATH)

app = Celery('shport-enrol')

app.conf.update(
    broker_url=REDIS_URI,
    result_backend=REDIS_URI
)

# Define periodic task schedule
app.conf.beat_schedule = {
    'scan_events': {
        'task': 'scan_events',
        'schedule': timedelta(seconds=RELOAD_TIMEOUT_SECONDS)
    }
}

import workers.tasks  # noqa
