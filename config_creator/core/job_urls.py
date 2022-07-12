from core.views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path(
        "add/",
        login_required(editjobview),
        name="job-add",
    ),
    path(
        "<int:pk>/update/",
        login_required(editjobview),
        name="job-update",
    ),
    path(
        "<int:pk>/delete/",
        login_required(jobdeleteview),
        name="job-delete",
    ),
    path(
        "",
        login_required(jobsview),
        name="jobs",
    ),
    path(
        "<int:pk>/download/",
        login_required(jobdownload),
        name="job-download",
    ),
    path(
        "<int:job_id>/property/",
        login_required(editjobproperty),
        name="job-property-add",
    ),
    path(
        "<int:job_id>/property/<int:pk>/",
        login_required(editjobproperty),
        name="job-property-update",
    ),
]
