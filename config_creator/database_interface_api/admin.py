import re

from .models import *
from core.models import BigQueryDataType
from database_interface_api.dbhelper import get_database_schema, get_schema
from database_interface_api.views import get_connection
from django.contrib import admin


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "get_connectiontype",
        "get_username",
    ]
    search_fields = ["email", "name"]
    actions = ["refresh"]
    ordering = ["connectiontype", "name"]

    def get_connectiontype(self, obj):
        return obj.connectiontype.description

    get_connectiontype.admin_order_field = "connectiontype"
    get_connectiontype.short_description = "Connection Type"

    def get_username(self, obj):
        return obj.user.email

    get_username.admin_order_field = "username"
    get_username.short_description = "User Name"

    def refresh(self, request, queryset):
        for connection in queryset:
            schema = get_schema(
                get_connection(
                    connection.user_id,
                    connection.id,
                )
            )

            for dataset in schema.get("result", {}):
                if not Dataset.objects.filter(
                    connection=connection,
                    name=dataset.get("name"),
                ).exists():
                    indb_dataset = Dataset(
                        connection=connection,
                        name=dataset.get("name"),
                    )
                else:
                    indb_dataset = Dataset.objects.get(
                        connection=connection,
                        name=dataset.get("name"),
                    )

                indb_dataset.save()

                # delete all tables for dataset - clear up db because
                # we won't be able to tell if a table has been deleted
                # by checking source.
                Table.objects.filter(
                    dataset=indb_dataset,
                ).delete()

                dataset_schema = get_database_schema(
                    get_connection(
                        connection.user_id,
                        connection.id,
                    ),
                    dataset.get("name"),
                )

                for table in dataset_schema.get("result", {}):
                    if not Table.objects.filter(
                        dataset=indb_dataset,
                        name=table.get("name"),
                    ).exists():
                        indb_table = Table(
                            dataset=indb_dataset,
                            name=table.get("name"),
                        )
                    else:
                        indb_table = Table.objects.get(
                            dataset=indb_dataset,
                            name=table.get("name"),
                        )

                    indb_table.save()

                    for column in table.get("content", []):
                        m = re.search(
                            r"^(\w+)(?:<.+)?$", column.get("data_type"), re.IGNORECASE
                        )
                        source_data_type = m.group(1).upper() if m else ""
                        data_type = (
                            BigQueryDataType.objects.get(name=source_data_type)
                            if BigQueryDataType.objects.filter(
                                name=source_data_type
                            ).exists()
                            else None
                        )

                        if not Column.objects.filter(
                            table=indb_table,
                            name=column.get("column_name"),
                        ).exists():
                            indb_column = Column(
                                table=indb_table,
                                name=column.get("column_name"),
                                data_type=data_type,
                                position=column.get("ordinal_position"),
                                is_nullable=column.get("is_nullable"),
                            )
                        else:
                            indb_column = Column.objects.get(
                                table=indb_table,
                                name=column.get("column_name"),
                                data_type=data_type,
                                position=column.get("ordinal_position"),
                                is_nullable=column.get("is_nullable"),
                            )

                        indb_column.save()

    refresh.short_description = "Refresh Connection Schema"


@admin.register(ConnectionType)
class ConnectionTypeAdmin(admin.ModelAdmin):
    list_display = [
        "description",
    ]


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "get_connection",
    ]
    list_filter = ["connection"]
    search_fields = ["name"]
    ordering = ["connection", "name"]

    def get_connection(self, obj):
        return obj.connection.name

    get_connection.admin_order_field = "connection"
    get_connection.short_description = "Connection Name"


class FieldInLine(admin.TabularInline):
    model = Column
    extra = 1
    max_num = 1


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "get_dataset",
    ]
    list_filter = ["dataset"]
    search_fields = ["name"]
    ordering = ["dataset", "name"]
    inlines = [FieldInLine]

    def get_dataset(self, obj):
        return obj.dataset.name

    get_dataset.admin_order_field = "dataset"
    get_dataset.short_description = "Dataset Name"
