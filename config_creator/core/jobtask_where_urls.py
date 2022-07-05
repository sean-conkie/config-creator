from core.views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

# urls will be suffixed job/<int:job_id>/task/<int:task_id>/
urlpatterns = [
    path(
        "where/condition/add/",
        login_required(editconditionview),
        name="job-task-where-condition-add",
    ),
    path(
        "where/condition/<int:pk>/update/",
        login_required(editconditionview),
        name="job-task-where-condition-update",
    ),
    path(
        "where/condition/<int:pk>/delete/",
        login_required(conditiondeleteview),
        name="job-task-where-condition-delete",
    ),
]
