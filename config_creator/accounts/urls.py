from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path


urlpatterns = [
    path("profile/", login_required(ProfileView.as_view()), name="profile"),
    path(
        "connections/",
        login_required(connectionsview),
        name="connections",
    ),
    path(
        "connection/",
        login_required(editconnectionview),
        name="connection-add",
    ),
    path(
        "connection/<int:pk>/",
        login_required(editconnectionview),
        name="connection-update",
    ),
    path(
        "connection/<int:pk>/delete/",
        login_required(ConnectionDeleteView.as_view()),
        name="connection-delete",
    ),
    path(
        "repositories/",
        login_required(repositoriesview),
        name="repositories",
    ),
    path(
        "repository/change/",
        login_required(editrepositoryview),
        name="repository-change",
    ),
    path(
        "repository/",
        login_required(repositoryview),
        name="repository-add",
    ),
    path(
        "repository/<int:pk>/",
        login_required(repositoryview),
        name="repository-update",
    ),
    path(
        "repository/<int:pk>/delete/",
        login_required(RepositoryDeleteView.as_view()),
        name="repository-delete",
    ),
]
