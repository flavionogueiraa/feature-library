import time

from celery import shared_task


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 4},
    retry_backoff=2,
)
def flaky_task(self, succeed_after=2):
    """Task instável que falha de propósito e se recupera via retry.

    Ela falha nas primeiras tentativas e só tem sucesso depois de
    `succeed_after` retentativas. Assim dá pra ver o Celery reagendando
    a task automaticamente (autoretry_for + retry_backoff).
    """
    succeed_after = int(succeed_after)
    attempt = self.request.retries  # 0 na primeira execução

    self.update_state(
        state="PROGRESS",
        meta={
            "attempt": attempt,
            "max_retries": 4,
            "message": f"Tentativa #{attempt + 1} em andamento...",
        },
    )
    time.sleep(1)

    if attempt < succeed_after:
        raise ValueError(
            f"Falha simulada na tentativa #{attempt + 1}. "
            f"O Celery vai tentar de novo automaticamente."
        )

    return {
        "attempts": attempt + 1,
        "message": (
            f"Sucesso após {attempt} retentativa(s)! "
            f"A task se recuperou sozinha."
        ),
    }
