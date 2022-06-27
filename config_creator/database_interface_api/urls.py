from .views import *
from django.urls import re_path

urlpatterns = [
    re_path(
        r"api\/schema\/(?P<connection_id>\d+)\/?$",
        SchemaView.as_view(),
        name="api-connection",
    ),
    re_path(
        r"api\/schema\/(?P<connection_id>\d+)\/(?P<database>\w+)$",
        SchemaView.as_view(),
        name="api-database",
    ),
]
