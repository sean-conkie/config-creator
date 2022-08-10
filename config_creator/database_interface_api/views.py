from .dbhelper import get_database_schema, get_schema
from .models import Connection, ConnectionType
from core.models import Job, JobTask, SourceTable
from django import views
from lib.baseclasses import ConnectionType as eConnectionType
from rest_framework import renderers, response, request, status, views

__all__ = [
    "SchemaView",
    "get_connection",
    "get_connections",
]


class SchemaView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]

    def get(
        self,
        request: request,
        connection_id: int = None,
        connection_name: int = None,
        database: str = None,
        task_id: int = None,
    ) -> response.Response:

        if database and connection_name:
            outp = get_database_schema(
                get_connection(
                    request.user.id,
                    connection_id,
                    connection_name,
                ),
                database,
                task_id,
                request.user.id,
            )

        elif connection_name:
            outp = get_schema(
                get_connection(
                    request.user.id,
                    connection_id,
                    connection_name,
                ),
                task_id,
                request.user.id,
            )
        elif database:
            outp = get_database_schema(
                get_connection(
                    request.user.id,
                    connection_id,
                ),
                database,
                task_id,
                request.user.id,
            )
        elif connection_id:
            outp = get_schema(
                get_connection(request.user.id, connection_id),
                task_id,
            )
        else:
            outp = get_connections(request, task_id)

        return response.Response(data=outp, status=status.HTTP_200_OK)


def get_connection(user_id: int, connection_id: int, name: str = None) -> dict:
    connection_id = int(connection_id)
    if connection_id < 1:
        connection_type = eConnectionType(connection_id)

        return {
            "id": connection_id,
            "name": name if name else "This Task",
            "credentials": None,
            "connection_string": None,
            "user_name": None,
            "host": None,
            "sid": None,
            "port": None,
            "schema": None,
            "secret_key": None,
            "connection_type": connection_type,
        }

    else:
        connection = Connection.objects.get(id=connection_id, user_id=user_id)
        connection_type = eConnectionType(connection.connectiontype.id)

        return {
            "id": connection.id,
            "name": connection.name,
            "credentials": connection.credentials,
            "connection_string": connection.connectionstring,
            "user_name": connection.user_name,
            "host": connection.host,
            "sid": connection.sid,
            "port": connection.port,
            "schema": connection.schema,
            "secret_key": connection.secret_key,
            "connection_type": connection_type,
        }


def get_connections(request: request, task_id: int = None) -> dict:
    connections = (
        Connection.objects.select_related().filter(user=request.user).order_by("name")
    )
    tree_source = []
    connection_map = {}
    for i, type in enumerate(ConnectionType.objects.all().order_by("description")):
        tree_source.append(
            {
                "name": type.description,
                "content": [],
                "type": "connection-type",
            }
        )
        connection_map[type.description] = i

    for connection in connections:
        tree_source[connection_map[connection.connectiontype.description]][
            "content"
        ].append(
            {
                "name": connection.name,
                "type": "connection",
                "id": connection.id,
            }
        )

    if task_id:
        source_tables = [
            {
                "name": table.source_project,
                "type": "connection",
                "id": 0,
            }
            for table in SourceTable.objects.filter(task_id=task_id).order_by(
                "source_project"
            )
            if table.source_project
        ]

        source_project = (
            JobTask.objects.select_related()
            .get(id=task_id)
            .job.get_property_object()
            .source_project
        )

        if source_project not in source_tables:
            source_tables.extend(
                [
                    {
                        "name": source_project,
                        "type": "connection",
                        "id": 0,
                    }
                ]
            )

        source_tables = [dict(t) for t in {tuple(d.items()) for d in source_tables}]

        tree_source.append(
            {
                "name": "This Task",
                "content": source_tables,
                "type": "connection-type",
            }
        )

        job_properties = Job.objects.get(
            id=JobTask.objects.get(id=task_id).job_id
        ).get_property_object()
        if job_properties:
            tree_source.append(
                {
                    "name": "This Job",
                    "content": [
                        {
                            "name": job_properties.target_project,
                            "type": "connection",
                            "id": -1,
                        }
                    ],
                    "type": "connection-type",
                }
            )

    return {"result": tree_source}
