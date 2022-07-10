from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path(
        "field/<int:pk>/delete/",
        login_required(FieldView.as_view()),
        name="api-field-delete",
    ),
    path(
        "task/<int:task_id>/connection/<int:connection_id>/dataset/<str:dataset>/table/<str:table_name>/copy/",
        login_required(copytable),
        name="api-table-copy",
    ),
]
