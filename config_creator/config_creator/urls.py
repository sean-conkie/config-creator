from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.static import serve as staticserveview
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("core.urls")),
    path("api/", include("database_interface_api.urls")),
    path("", include("django.contrib.auth.urls")),
    path("api/", include("core_api.urls")),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(
        r"^media/(?P<path>.*)$", staticserveview, {"document_root": settings.MEDIA_ROOT}
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
