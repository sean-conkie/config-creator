from core.views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

# urls will be suffixed job/<int:job_id>/task/<int:task_id>/
urlpatterns = [
    path(
        "join/add/",
        login_required(editjoinview),
        name="job-task-join-add",
    ),
    path(
        "join/<int:pk>/",
        login_required(editjoinview),
        name="job-task-join",
    ),
    path(
        "join/<int:pk>/delete/",
        login_required(joindeleteview),
        name="job-task-join-delete",
    ),
    path(
        "join/<int:join_id>/condition/add/",
        login_required(editconditionview),
        name="job-task-join-condition-add",
    ),
    path(
        "join/<int:join_id>/condition/<int:pk>/update/",
        login_required(editconditionview),
        name="job-task-join-condition-update",
    ),
    path(
        "join/<int:join_id>/condition/<int:pk>/delete/",
        login_required(conditiondeleteview),
        name="job-task-join-condition-delete",
    ),
]
