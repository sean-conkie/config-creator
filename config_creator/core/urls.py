from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path("", login_required(index), name="home"),
    path(
        "repositories/",
        login_required(repositoriesview),
        name="repository-list",
    ),
    path(
        "repositories/<int:pk>/pull/",
        login_required(pullrepository),
        name="repository-pull",
    ),
    path(
        "repository/new/pull/",
        login_required(pullnewrepository),
        name="repository-pull-new",
    ),
    path(
        "file/upload/",
        login_required(fileselect),
        name="file-upload",
    ),
]
