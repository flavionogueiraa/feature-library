import random
import time

from celery import shared_task

# --- Tasks para a demonstração de CHAIN (execução em sequência) ----------
# Um pipeline ETL clássico: extrair -> transformar -> carregar.
# O resultado de cada etapa é passado automaticamente para a próxima.


@shared_task
def extract():
    """Etapa 1 do chain: 'extrai' uma lista de números."""
    time.sleep(2)
    return [1, 2, 3, 4, 5]


@shared_task
def transform(numbers):
    """Etapa 2 do chain: recebe o resultado da etapa anterior e transforma."""
    time.sleep(2)
    return [n * 10 for n in numbers]


@shared_task
def load(numbers):
    """Etapa 3 do chain: 'carrega' o resultado final (a soma)."""
    time.sleep(2)
    return {"total": sum(numbers), "items": numbers}


# --- Task para a demonstração de GROUP (execução em paralelo) ------------


@shared_task(bind=True)
def crunch_number(self, n):
    """Processa um número com duração aleatória.

    Disparada em paralelo (group), cada instância roda num worker e
    termina em momentos diferentes — ótimo pra mostrar paralelismo.
    """
    duration = random.uniform(1.5, 5.0)
    time.sleep(duration)
    return {
        "n": n,
        "result": n * n,
        "duration": round(duration, 2),
    }
