import json
from datetime import datetime

import redis
from celery import shared_task
from django.conf import settings

HEARTBEAT_KEY = "celery_demo:heartbeats"
HEARTBEAT_MAX = 15


def get_redis():
    """Cliente Redis apontando para o mesmo broker do Celery."""
    return redis.from_url(settings.CELERY_BROKER_URL)


@shared_task
def heartbeat_task():
    """Task periódica disparada pelo Celery Beat.

    A cada execução agendada ela grava um 'batimento' numa lista no Redis.
    A página lê essa lista e mostra que o Beat está disparando tasks
    sozinho, no intervalo configurado — sem ninguém clicar em nada.
    """
    client = get_redis()
    beat = json.dumps(
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "message": "Batimento automático do Celery Beat",
        }
    )
    client.lpush(HEARTBEAT_KEY, beat)
    client.ltrim(HEARTBEAT_KEY, 0, HEARTBEAT_MAX - 1)
    return "ok"
