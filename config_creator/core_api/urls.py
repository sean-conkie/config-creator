from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path


urlpatterns = [
    path(
        "job/<int:pk>/delete/",
        login_required(JobView.as_view()),
        name="api-job-delete",
    ),
    path(
        "job/<int:job_id>/task/<int:pk>/delete/",
        login_required(JobTaskView.as_view()),
        name="api-task-delete",
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
    re_path(
        r"task\/(?P<task_id>\d+)\/connection\/(?P<connection_id>-?\d+)\/dataset\/(?P<dataset>[\w\-\d]+)\/table\/(?P<table_name>[\w\-\d]+(?: [\w\-\d]+)?)\/copy\/",
        login_required(copytable),
        name="api-table-copy",
    ),
    re_path(
        r"task\/(?P<task_id>\d+)\/connection\/(?P<connection_name>[\w\-\d]+)\/dataset\/(?P<dataset>[\w\-\d]+)\/table\/(?P<table_name>[\w\-\d]+(?: [\w\-\d]+)?)\/copy\/",
        login_required(copytable),
        name="api-table-copy-alt",
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
        "task/<int:task_id>/sk/add/",
        login_required(create_sk),
        name="api-sk-add",
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
    path(
        "job/<int:job_id>/task/<int:task_id>/delta/add/",
        login_required(DeltaConditionView.as_view()),
        name="api-delta-add",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/delta/<int:pk>/update/",
        login_required(DeltaConditionView.as_view()),
        name="api-delta-update",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/delta/<int:pk>/delete/",
        login_required(DeltaConditionView.as_view()),
        name="api-delta-delete",
    ),
    path(
        "task/<int:task_id>/position/",
        login_required(newfieldposition),
        name="api-position",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/predecessor/add/",
        login_required(PredecessorView.as_view()),
        name="api-predecessor-add",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/predecessor/<int:pk>/update/",
        login_required(PredecessorView.as_view()),
        name="api-predecessor-update",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/predecessor/<int:pk>/delete/",
        login_required(PredecessorView.as_view()),
        name="api-predecessor-delete",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/predecessor/<int:pk>/",
        login_required(PredecessorView.as_view()),
        name="api-predecessor",
    ),
    path(
        "job/<int:job_id>/task/<int:task_id>/predecessor/tasks/",
        login_required(possibletasks),
        name="api-predecessor-tasks",
    ),
    path(
        "file/upload/",
        login_required(UploadFileView.as_view()),
        name="api-file-upload",
    ),
    path(
        "repositories/<int:pk>/pull/",
        login_required(pullrepository),
        name="api-repo-pull",
    ),
    re_path(
        r"repositories\/(?P<pk>\d+)\/pull\/(?P<branch>[\w\/\-\d]+)\/",
        login_required(pullrepository),
        name="api-repo-pull-branch",
    ),
    path(
        "task/<int:pk>/summary/",
        login_required(tasksummary),
        name="api-task-summary",
    ),
    path(
        "function/type/",
        login_required(function_type),
        name="api-function-type",
    ),
    path(
        "function/type/<str:function_type>/",
        login_required(function_by_type),
        name="api-function-by-type",
    ),
]
