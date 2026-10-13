from celery import Celery

from app.config import REDIS_URL

celery_app = Celery(
    "media_processor",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_track_started=True,   # permite distinguir "pendiente" de "procesando"
    result_expires=3600,       # los resultados se borran de Redis tras 1 hora
)