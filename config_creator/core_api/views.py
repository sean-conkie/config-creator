from core.models import Field, JobTask
from database_interface_api.dbhelper import get_table
from database_interface_api.views import get_connection
from django import views
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import renderers, response, request, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class FieldView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request: request, pk: int) -> response.Response:
        """
        > This function deletes a field from the database

        Args:
          request (request): request - this is the request object that is passed to the view.
          pk (int): The primary key of the field to be deleted.

        Returns:
          A response object with the data and status.
        """

        field = Field.objects.get(id=pk)
        if field:
            outp = {
                "message": f"Field '{field.name}' deleted.",
                "type": "success",
            }
            field.delete()
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Field with id '{pk}' does not exist.",
                "type": "error",
            }
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data=outp, status=return_status)


@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def copytable(request, task_id, connection_id, dataset, table_name):
    try:
        task = JobTask.objects.get(id=task_id)
    except ObjectDoesNotExist:
        return response.Response(
            data={
                "message": f"JobTask for id {task_id} not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    table = get_table(get_connection(request, connection_id), dataset, table_name)

    for column in table.get("result", {}).get("content", []):
        field = Field(
            name=column.get("column_name"),
            source_column=column.get("column_name"),
            source_name=f"{column.get('dataset')}.{column.get('table_name')}",
            task=task,
        )
        field.save()
        column["id"] = field.id

    return response.Response(data=table, status=status.HTTP_200_OK)
