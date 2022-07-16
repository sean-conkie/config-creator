from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path(
        "field/<int:pk>/delete/",
        login_required(FieldView.as_view()),
        name="api-field-delete",
    ),
    path(
        "job/<int:pk>/delete/",
        login_required(JobView.as_view()),
        name="api-job-delete",
    ),
    path(
        "task/<int:task_id>/connection/<int:connection_id>/dataset/<str:dataset>/table/<str:table_name>/copy/",
        login_required(copytable),
        name="api-table-copy",
    ),
    path(
        "data-type-comparison/<str:source>/<str:target>/<str:column>/",
        login_required(datatypecomparison),
        name="api-data-type-comparison",
    ),
    path(
        "task/<int:task_id>/field/<int:field_id>/position/<int:position>/update/",
        login_required(fieldpositionchange),
        name="api-task-field-position-update",
    ),
]
