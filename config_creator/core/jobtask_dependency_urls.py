from core.views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

# urls will be suffixed job/<int:job_id>/task/<int:task_id>/
urlpatterns = [
    path(
        "dependency/add/",
        login_required(adddependencyview),
        name="job-task-dependency-add",
    ),
    path(
        "dependency/<int:pk>/delete/",
        login_required(dependencydeleteview),
        name="job-task-dependency-delete",
    ),
    path(
        "dependency/<int:dependency_id>/task/<int:pk>/",
        login_required(jobtaskview),
        name="job-task-dependency-task",
    ),
]
