from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path(
        "schema/",
        login_required(SchemaView.as_view()),
        name="api-connections",
    ),
    path(
        "task/<int:task_id>/schema/",
        login_required(SchemaView.as_view()),
        name="api-connections-task",
    ),
    path(
        "schema/<int:connection_id>/",
        login_required(SchemaView.as_view()),
        name="api-schema",
    ),
    path(
        "task/<int:task_id>/schema/<int:connection_id>/<str:connection_name>/",
        login_required(SchemaView.as_view()),
        name="api-task-schema",
    ),
    path(
        "schema/<int:connection_id>/<str:database>/",
        login_required(SchemaView.as_view()),
        name="api-database",
    ),
    path(
        "task/<int:task_id>/schema/<int:connection_id>/<str:connection_name>/<str:database>/",
        login_required(SchemaView.as_view()),
        name="api-task-database",
    ),
]
