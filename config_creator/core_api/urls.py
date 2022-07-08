from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path(
        "field/<int:pk>/delete/",
        login_required(FieldView.as_view()),
        name="api-field-delete",
    ),
]
