import json

from celery import chain, group
from celery.result import AsyncResult
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView

from celery_demonstration.tasks import (
    HEARTBEAT_KEY,
    crunch_number,
    extract,
    flaky_task,
    get_redis,
    load,
    progress_task,
    transform,
)


class CeleryDemoView(TemplateView):
    """Página interativa de demonstração do Celery."""

    template_name = "celery_demonstration/demo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flower_url"] = settings.FLOWER_URL
        return context


@require_POST
def dispatch_progress(request):
    """Dispara a task longa com progresso. Retorna o id na hora."""
    result = progress_task.delay(total_steps=10, step_seconds=1)
    return JsonResponse({"task_id": result.id})


@require_POST
def dispatch_flaky(request):
    """Dispara a task instável que se recupera via retry."""
    result = flaky_task.delay(succeed_after=2)
    return JsonResponse({"task_id": result.id})


@require_POST
def dispatch_chain(request):
    """Dispara um chain (extract -> transform -> load), em sequência.

    Retorna os ids de cada etapa, na ordem, percorrendo os `parent`s do
    AsyncResult final — assim o frontend acompanha etapa por etapa.
    """
    workflow = chain(extract.s(), transform.s(), load.s())
    result = workflow.apply_async()

    # O resultado é o da última etapa; .parent encadeia até a primeira.
    ids = []
    node = result
    while node is not None:
        ids.append(node.id)
        node = node.parent
    ids.reverse()  # ordem de execução: extract, transform, load

    return JsonResponse(
        {
            "task_ids": ids,
            "labels": ["extract", "transform", "load"],
        }
    )


@require_POST
def dispatch_group(request):
    """Dispara um group: várias tasks em paralelo. Retorna todos os ids."""
    numbers = [2, 4, 6, 8, 10]
    job = group(crunch_number.s(n) for n in numbers)
    result = job.apply_async()
    return JsonResponse(
        {
            "task_ids": [child.id for child in result.children],
            "numbers": numbers,
        }
    )


@require_GET
def task_status(request, task_id):
    """Consulta o estado de uma task no result backend (Redis)."""
    result = AsyncResult(task_id)
    info = result.info

    # `info` pode ser uma exceção (em FAILURE) — serializa como texto.
    if isinstance(info, Exception):
        info = {"message": str(info)}
    elif not isinstance(info, dict):
        info = {"value": info}

    return JsonResponse(
        {
            "task_id": task_id,
            "state": result.state,
            "ready": result.ready(),
            "successful": result.successful() if result.ready() else None,
            "info": info,
        }
    )


@require_GET
def heartbeats(request):
    """Lê os últimos batimentos gravados pelo Celery Beat no Redis."""
    client = get_redis()
    raw = client.lrange(HEARTBEAT_KEY, 0, -1)
    beats = [json.loads(item) for item in raw]
    return JsonResponse({"beats": beats})
