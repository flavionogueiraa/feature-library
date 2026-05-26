import os
from celery import Celery
from celery.schedules import schedule
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "feature_library.settings")
app = Celery("feature_library")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Agendamento do Celery Beat: dispara o heartbeat a cada 10 segundos
# para a página de demonstração mostrar tasks periódicas em ação.
app.conf.beat_schedule = {
    "demo-heartbeat": {
        "task": "celery_demonstration.tasks.heartbeat_task.heartbeat_task",
        "schedule": schedule(run_every=10.0),
    },
}
