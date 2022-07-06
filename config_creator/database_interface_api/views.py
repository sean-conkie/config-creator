from .dbhelper import get_database_schema, get_schema
from .models import Connection, ConnectionType
from django import views
from lib.baseclasses import ConnectionType as eConnectionType
from rest_framework import renderers, response, request, status, views


class SchemaView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]

    def get(
        self, request: request, connection_id: int = None, database: str = None
    ) -> response.Response:

        if database:
            outp = get_database_schema(get_connection(request, connection_id), database)
        elif connection_id:
            outp = get_schema(get_connection(request, connection_id))
        else:
            outp = get_connections(request)

        return response.Response(data=outp, status=status.HTTP_200_OK)


def get_connection(request, connection_id: int) -> dict:

    connection = Connection.objects.get(id=connection_id, user=request.user)
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


def get_connections(request: request) -> dict:
    """
    > This function returns a dictionary of connections for a user, grouped by connection type

    Args:
      request (request): request

    Returns:
      A dictionary of connections
    """
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

    return {"result": tree_source}
