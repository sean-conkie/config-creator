from requests import ConnectTimeout
from .dbhelper import get_database_schema, get_schema
from .models import Connection
from django import views
from lib.baseclasses import ConnectionType
from rest_framework import renderers, response, request, status, views


class SchemaView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]

    def get(
        self, request: request, connection_id: int, database: str = None
    ) -> response:

        connection = Connection.objects.get(id=connection_id)
        connection_type = ConnectionType(connection.connectiontype.id)

        if database:
            print("returning database schema")
            outp = get_database_schema(
                connection.connectionstring, connection_type, database
            )
        else:
            print("returning connection schema")
            outp = get_schema(connection.connectionstring, connection_type)

        return response.Response(data=outp, status=status.HTTP_200_OK)
