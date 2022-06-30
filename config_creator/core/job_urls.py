from core.views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path(
        "add/",
        login_required(JobCreateView.as_view()),
        name="job-add",
    ),
    path(
        "<int:pk>/update/",
        login_required(JobUpdateView.as_view()),
        name="job-update",
    ),
    path(
        "<int:pk>/delete/",
        login_required(JobDeleteView.as_view()),
        name="job-delete",
    ),
    path(
        "jobs/",
        login_required(jobsview),
        name="jobs",
    ),
]
