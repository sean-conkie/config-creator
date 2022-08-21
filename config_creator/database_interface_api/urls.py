from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

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
        "job/<int:job_id>/schema/",
        login_required(SchemaView.as_view()),
        name="api-connections-job",
    ),
    path(
        "schema/<int:connection_id>/",
        login_required(SchemaView.as_view()),
        name="api-schema",
    ),
    re_path(
        r"task\/(?P<task_id>\d+)\/schema\/(?P<connection_id>-?\d+)\/(?P<connection_name>[\w\-\d]+)\/$",
        login_required(SchemaView.as_view()),
        name="api-task-schema",
    ),
    re_path(
        r"job\/(?P<job_id>\d+)\/schema\/(?P<connection_id>-?\d+)\/(?P<connection_name>[\w\-\d]+)\/$",
        login_required(SchemaView.as_view()),
        name="api-job-schema",
    ),
    path(
        "schema/<int:connection_id>/<str:database>/",
        login_required(SchemaView.as_view()),
        name="api-database",
    ),
    re_path(
        r"task\/(?P<task_id>\d+)\/schema\/(?P<connection_id>-?\d+)\/(?P<connection_name>[\w\-\d]+)\/(?P<database>[\w\-\d]+)\/$",
        login_required(SchemaView.as_view()),
        name="api-task-database",
    ),
    re_path(
        r"job\/(?P<job_id>\d+)\/schema\/(?P<connection_id>-?\d+)\/(?P<connection_name>[\w\-\d]+)\/(?P<database>[\w\-\d]+)\/$",
        login_required(SchemaView.as_view()),
        name="api-job-database",
    ),
]
