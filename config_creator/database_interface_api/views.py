from .dbhelper import AppClient, get_database_schema, get_schema
from .models import Connection, ConnectionType
from accounts.models import User
from core.models import Job, JobTask, SourceTable
from django import views
from django.db.models import Q
from rest_framework import renderers, response, request, status, views

__all__ = [
    "SchemaView",
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
        table: str = None,
        job_id: int = None,
        task_id: int = None,
        is_full_schema: str = None,
    ) -> response.Response:
        if connection_name:
            connection = Connection.objects.get(
                name=connection_name,
            )
        elif connection_id:
            connection = Connection.objects.get(
                id=connection_id,
            )
        else:
            connection = None

        if connection_id == "-1" and task_id:
            job_id = JobTask.objects.get(id=task_id).job_id

        if connection:
            connection.id = connection_id

        if database:
            outp = get_database_schema(
                connection,
                AppClient(
                    connection,
                    database,
                    job_id=job_id,
                    task_id=task_id,
                ),
                table,
            )
        elif connection:
            outp = get_schema(
                connection,
                AppClient(
                    connection,
                    job_id=job_id,
                    task_id=task_id,
                ),
            )
        else:
            outp = get_connections(request, job_id, task_id, is_full_schema)

        return response.Response(data=outp, status=status.HTTP_200_OK)


def get_connections(
    request: request,
    job_id: int = None,
    task_id: int = None,
    is_full_schema: str = None,
) -> dict:
    connections = (
        Connection.objects.select_related()
        .filter(Q(user=request.user) | Q(user=User.objects.get(email="admin@root.com")))
        .order_by("name")
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

        source_project = {
            "name": (
                JobTask.objects.select_related()
                .get(id=task_id)
                .job.get_property_object()
                .source_project
            ),
            "type": "connection",
            "id": 0,
        }

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

        job_id = JobTask.objects.get(id=task_id).job_id

    if job_id:
        job_properties = Job.objects.get(id=job_id).get_property_object()
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
