from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import include, path

urlpatterns = [
    path("", login_required(index), name="home"),
    path("job/", include("core.job_urls")),
    path("", include("core.file_upload_urls")),
    path("job/<int:job_id>/", include("core.jobtask_urls")),
    path("job/<int:job_id>/task/<int:task_id>/", include("core.jobtask_field_urls")),
    path("job/<int:job_id>/task/<int:task_id>/", include("core.jobtask_join_urls")),
    path("job/<int:job_id>/task/<int:task_id>/", include("core.jobtask_where_urls")),
    path("job/<int:job_id>/task/<int:task_id>/", include("core.jobtask_delta_urls")),
]
