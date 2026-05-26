import time

from celery import shared_task


@shared_task(bind=True)
def progress_task(self, total_steps=10, step_seconds=1):
    """Simula um trabalho longo reportando progresso ao vivo.

    A cada passo a task atualiza seu estado para PROGRESS com metadados
    (passo atual, total e uma mensagem). O frontend consulta esse estado
    via polling e desenha a barra de progresso em tempo real.
    """
    total_steps = int(total_steps)
    step_seconds = float(step_seconds)

    logs = []
    for current in range(1, total_steps + 1):
        time.sleep(step_seconds)
        message = f"Processando lote {current} de {total_steps}..."
        logs.append(message)
        self.update_state(
            state="PROGRESS",
            meta={
                "current": current,
                "total": total_steps,
                "percent": round(current / total_steps * 100),
                "message": message,
                "logs": logs,
            },
        )

    return {
        "current": total_steps,
        "total": total_steps,
        "percent": 100,
        "message": "Trabalho concluído com sucesso!",
        "logs": logs,
    }
