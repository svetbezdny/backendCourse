from celery import Celery

from src.config import settings

celery_app = Celery(
    "celery_app",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["src.tasks.tasks"],
    broker_connection_retry_on_startup=True,
)

celery_app.conf.beat_schedule = {
    "send_email": {
        "task": "bookings_today_checkin",
        "schedule": 5,
    }
}
