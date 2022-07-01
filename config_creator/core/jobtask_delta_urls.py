from core.views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

# urls will be suffixed job/<int:job_id>/task/<int:task_id>/
urlpatterns = [
    path(
        "delta/add/",
        login_required(editdeltaview),
        name="job-task-delta-add",
    ),
    path(
        "delta/<int:pk>/delete/",
        login_required(deltadeleteview),
        name="job-task-delta-delete",
    ),
    path(
        "delta/<int:pk>/update/",
        login_required(editdeltaview),
        name="job-task-delta-update",
    ),
]
