from django.apps import AppConfig

class CeleryDemonstrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celery_demonstration'

    def ready(self):
        import celery_demonstration.signals
