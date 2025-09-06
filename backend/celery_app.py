from celery import Celery
from config import REDIS_URL

# Create Celery instance
celery_app = Celery(
    "multipost_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks.publish_tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Task routing
celery_app.conf.task_routes = {
    "tasks.publish_tasks.publish_to_facebook": {"queue": "facebook"},
    "tasks.publish_tasks.publish_to_instagram": {"queue": "instagram"},
    "tasks.publish_tasks.publish_to_tiktok": {"queue": "tiktok"},
    "tasks.publish_tasks.refresh_tokens": {"queue": "maintenance"},
}

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "refresh-expired-tokens": {
        "task": "tasks.publish_tasks.refresh_expired_tokens",
        "schedule": 3600.0,  # Every hour
    },
    "cleanup-old-logs": {
        "task": "tasks.publish_tasks.cleanup_old_logs",
        "schedule": 86400.0,  # Every day
    },
}

if __name__ == "__main__":
    celery_app.start()
