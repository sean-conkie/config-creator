from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import PartitionView
from .views import orderpositionchange
from .views import JoinView

urlpatterns = [
    path(
        "job/<int:pk>/delete/",
        login_required(JobView.as_view()),
        name="api-job-delete",
    ),
    path(
        "condition/<int:pk>/delete/",
        login_required(ConditionView.as_view()),
        name="api-condition-delete",
    ),
    path(
        "source_table/<int:pk>/delete/",
        login_required(SourceTableView.as_view()),
        name="api-source-table-delete",
    ),
    path(
        "source_table/<int:pk>/update/",
        login_required(SourceTableView.as_view()),
        name="api-source-table-update",
    ),
    path(
        "source_table/<int:pk>/",
        login_required(SourceTableView.as_view()),
        name="api-source-table",
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
        "data-type-map/<str:source>/",
        login_required(datatypemap),
        name="api-data-type-map",
    ),
    path(
        "task/<int:task_id>/field/<int:field_id>/position/<int:position>/update/",
        login_required(fieldpositionchange),
        name="api-task-field-position-update",
    ),
    path(
        "task/<int:task_id>/history-order/<int:order_id>/position/<int:position>/update/",
        login_required(orderpositionchange),
        name="api-task-history-order-position-update",
    ),
    path(
        "field/<int:pk>/",
        login_required(FieldView.as_view()),
        name="api-field",
    ),
    path(
        "field/<int:pk>/delete/",
        login_required(FieldView.as_view()),
        name="api-field-delete",
    ),
    path(
        "task/<int:task_id>/field/add/",
        login_required(FieldView.as_view()),
        name="api-field-add",
    ),
    path(
        "task/<int:task_id>/field/<int:pk>/update/",
        login_required(FieldView.as_view()),
        name="api-field-update",
    ),
    path(
        "diving-column/<int:pk>/delete/",
        login_required(DrivingColumnView.as_view()),
        name="api-diving-column-delete",
    ),
    path(
        "partition/<int:pk>/delete/",
        login_required(PartitionView.as_view()),
        name="api-partition-delete",
    ),
    path(
        "history-order/<int:pk>/delete/",
        login_required(HistoryOrderView.as_view()),
        name="api-history-order-delete",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/join/<int:pk>/",
        login_required(JoinView.as_view()),
        name="api-join",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/join/add/",
        login_required(JoinView.as_view()),
        name="api-join-add",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/join/<int:pk>/update/",
        login_required(JoinView.as_view()),
        name="api-join-update",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/join/<int:pk>/delete/",
        login_required(JoinView.as_view()),
        name="api-join-delete",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/condition/<int:pk>/",
        login_required(ConditionView.as_view()),
        name="api-condition",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/condition/add/",
        login_required(ConditionView.as_view()),
        name="api-condition-add",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/join/<int:join_id>/condition/add/",
        login_required(ConditionView.as_view()),
        name="api-join-condition-add",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/condition/<int:pk>/update/",
        login_required(ConditionView.as_view()),
        name="api-condition-update",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/condition/<int:pk>/delete/",
        login_required(ConditionView.as_view()),
        name="api-condition-delete",
    ),
]
