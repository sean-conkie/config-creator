from accounts import views as account_views
from core import views as core_views
from database_interface_api import views as api_views
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.static import serve as staticserveview
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path("", login_required(core_views.index), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", include(router.urls)),
    path("accounts/profile/", account_views.ProfileView.as_view(), name="profile"),
    path(
        "accounts/connections/",
        login_required(account_views.connectionsview),
        name="connections",
    ),
    path(
        "accounts/connection/change/",
        login_required(account_views.editconnectionview),
        name="connection-change",
    ),
    path(
        "accounts/connection/",
        login_required(account_views.connectionview),
        name="connection-add",
    ),
    path(
        "accounts/connection/<int:pk>/",
        login_required(account_views.connectionview),
        name="connection-update",
    ),
    path(
        "accounts/connection/<int:pk>/delete/",
        login_required(account_views.ConnectionDeleteView.as_view()),
        name="connection-delete",
    ),
    path(
        "accounts/repositories/",
        login_required(account_views.repositoriesview),
        name="repositories",
    ),
    path(
        "repositories/",
        login_required(core_views.repositoriesview),
        name="repository-list",
    ),
    path(
        "repositories/<int:pk>/pull/",
        login_required(core_views.pullrepository),
        name="repository-pull",
    ),
    path(
        "accounts/repository/change/",
        login_required(account_views.editrepositoryview),
        name="repository-change",
    ),
    path(
        "accounts/repository/new/pull/",
        login_required(core_views.pullnewrepository),
        name="repository-pull-new",
    ),
    path(
        "accounts/repository/",
        login_required(account_views.repositoryview),
        name="repository-add",
    ),
    path(
        "accounts/repository/<int:pk>/",
        login_required(account_views.repositoryview),
        name="repository-update",
    ),
    path(
        "accounts/repository/<int:pk>/delete/",
        login_required(account_views.RepositoryDeleteView.as_view()),
        name="repository-delete",
    ),
    re_path(
        r"api\/schema\/(?P<connection_id>\d+)\/?$",
        api_views.SchemaView.as_view(),
    ),
    re_path(
        r"api\/schema\/(?P<connection_id>\d+)\/(?P<database>\w+)$",
        api_views.SchemaView.as_view(),
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(
        r"^media/(?P<path>.*)$", staticserveview, {"document_root": settings.MEDIA_ROOT}
    ),
]
