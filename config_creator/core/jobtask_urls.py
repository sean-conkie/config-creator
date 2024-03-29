from core.views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

# urls will be suffixed job/<int:job_id>/
urlpatterns = [
    path(
        "",
        login_required(jobtasksview),
        name="job-tasks",
    ),
    path(
        "task/add/",
        login_required(editjobtaskview),
        name="job-task-add",
    ),
    path(
        "task/<int:pk>/update/",
        login_required(editjobtaskview),
        name="job-task-update",
    ),
    path(
        "task/<int:pk>/",
        login_required(jobtaskview),
        name="job-task",
    ),
    path(
        "task/<int:pk>/delete/",
        login_required(jobtaskdeleteview),
        name="job-task-delete",
    ),
    path(
        "task/<int:task_id>/condition/<int:pk>/delete/",
        login_required(conditiondeleteview),
        name="job-task-condition-delete",
    ),
    path(
        "task/<int:task_id>/property/",
        login_required(editjobtaskproperty),
        name="job-task-property-add",
    ),
    path(
        "task/<int:task_id>/property/<int:pk>/",
        login_required(editjobtaskproperty),
        name="job-task-property-update",
    ),
]
