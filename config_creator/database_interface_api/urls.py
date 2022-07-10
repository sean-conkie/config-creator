from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path(
        "schema/",
        login_required(SchemaView.as_view()),
        name="api-connections",
    ),
    path(
        "schema/<int:connection_id>/",
        login_required(SchemaView.as_view()),
        name="api-schema",
    ),
    path(
        "schema/<int:connection_id>/<str:database>/",
        login_required(SchemaView.as_view()),
        name="api-database",
    ),
]
