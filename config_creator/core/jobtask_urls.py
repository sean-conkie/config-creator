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
        login_required(JobTaskDeleteView.as_view()),
        name="job-task-delete",
    ),
]
