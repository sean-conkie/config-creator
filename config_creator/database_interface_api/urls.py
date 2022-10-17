from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

urlpatterns = [
    re_path(
        r"schema\/(?P<is_full_schema>true|false)\/$",
        login_required(SchemaView.as_view()),
        name="api-connections",
    ),
    re_path(
        r"task\/(?P<task_id>\d+)\/schema\/(?P<is_full_schema>true|false)\/$",
        login_required(SchemaView.as_view()),
        name="api-connections-task",
    ),
    re_path(
        r"job\/(?P<job_id>\d+)\/schema\/(?P<is_full_schema>true|false)\/$",
        login_required(SchemaView.as_view()),
        name="api-connections-job",
    ),
    re_path(
        r"schema\/(?P<connection_id>-?\d+)\/$",
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
    path(
        "schema/<int:connection_id>/<str:database>/<str:table>/",
        login_required(SchemaView.as_view()),
        name="api-database-table",
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
