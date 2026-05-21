from celery import shared_task


@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 5},
    bind=True,
)
def hello_celery_task2(self, algum_parametro):
    """Função simples de task celery."""
    print(dir(self))
    if algum_parametro == "fail":
        raise ValueError("Simulando falha para testar retry")
    print(f"Hello, Celery 2! O parâmetro recebido foi: {algum_parametro}")
