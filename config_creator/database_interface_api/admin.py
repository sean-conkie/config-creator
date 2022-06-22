from .models import *
from django.contrib import admin


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "get_connectiontype",
        "get_username",
    ]
    search_fields = ["email"]

    def get_connectiontype(self, obj):
        return obj.connectiontype.description

    get_connectiontype.admin_order_field = "connectiontype"
    get_connectiontype.short_description = "Connection Type"

    def get_username(self, obj):
        return obj.user.email

    get_username.admin_order_field = "username"
    get_username.short_description = "User Name"


@admin.register(ConnectionType)
class ConnectionTypeAdmin(admin.ModelAdmin):
    list_display = [
        "description",
    ]
