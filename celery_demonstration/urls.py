from django.urls import path

from . import views

app_name = "celery_demonstration"

urlpatterns = [
    path(
        "celery-demo/",
        views.CeleryDemoView.as_view(),
        name="demo",
    ),
    path(
        "celery-demo/dispatch/progress/",
        views.dispatch_progress,
        name="dispatch_progress",
    ),
    path(
        "celery-demo/dispatch/flaky/",
        views.dispatch_flaky,
        name="dispatch_flaky",
    ),
    path(
        "celery-demo/dispatch/chain/",
        views.dispatch_chain,
        name="dispatch_chain",
    ),
    path(
        "celery-demo/dispatch/group/",
        views.dispatch_group,
        name="dispatch_group",
    ),
    path(
        "celery-demo/status/<str:task_id>/",
        views.task_status,
        name="task_status",
    ),
    path(
        "celery-demo/heartbeats/",
        views.heartbeats,
        name="heartbeats",
    ),
]
