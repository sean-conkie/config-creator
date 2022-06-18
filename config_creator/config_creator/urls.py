"""config_creator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from accounts import views as account_views
from core import views as core_views
from database_interface_api import views as api_views
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path("", core_views.index, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", include(router.urls)),
    re_path(
        r"api\/schema\/(?P<connection_id>\d+)\/?$",
        api_views.SchemaView.as_view(),
    ),
    re_path(
        r"api\/schema\/(?P<connection_id>\d+)\/(?P<database>\w+)$",
        api_views.SchemaView.as_view(),
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
