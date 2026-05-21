from celery import shared_task


@shared_task()
def hello_celery_task(algum_parametro):
    """Função simples de task celery."""
    print(f"Hello, Celery! O parâmetro recebido foi: {algum_parametro}")
