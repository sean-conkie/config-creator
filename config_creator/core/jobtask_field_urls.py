from core.views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

# urls will be suffixed job/<int:job_id>/task/<int:task_id>/
urlpatterns = [
    path(
        "field/add/",
        login_required(editfieldview),
        name="job-task-field-add",
    ),
    path(
        "field/<int:pk>/",
        login_required(fieldview),
        name="job-task-field",
    ),
    path(
        "field/<int:pk>/delete/",
        login_required(fielddeleteview),
        name="job-task-field-delete",
    ),
    path(
        "field/<int:pk>/update/",
        login_required(editfieldview),
        name="job-task-field-update",
    ),
]
