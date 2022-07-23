from core.views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

# urls will be suffixed job/<int:job_id>/task/<int:task_id>/
urlpatterns = [
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
]
