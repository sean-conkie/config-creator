from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import re_path, path

urlpatterns = [
    path(
        "api/schema/",
        login_required(SchemaView.as_view()),
        name="api-connections",
    ),
    path(
        "api/schema/<int:connection_id>/",
        login_required(SchemaView.as_view()),
        name="api-schema",
    ),
    path(
        "api/schema/<int:connection_id>/<str:database>/",
        login_required(SchemaView.as_view()),
        name="api-database",
    ),
]
