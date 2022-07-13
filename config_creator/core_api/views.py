from core.models import (
    BigQueryDataType,
    DATA_TYPE_MAPPING,
    Field,
    changefieldposition,
    JobTask,
)
from database_interface_api.dbhelper import get_table
from database_interface_api.views import get_connection
from django import views
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
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
    """
    It takes a connection id, a dataset name, and a table name, and copies the table's columns into the
    database

    Args:
      request: The request object that was sent to the view.
      task_id: The id of the JobTask that we're copying the table to.
      connection_id: The id of the connection you want to use.
      dataset: The name of the dataset that contains the table you want to copy.
      table_name: The name of the table you want to copy.

    Returns:
      A list of columns in the table.
    """
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

    for i, column in enumerate(table.get("result", {}).get("content", [])):
        field = Field(
            name=column.get("column_name"),
            source_column=column.get("column_name"),
            source_name=f"{column.get('dataset')}.{column.get('table_name')}",
            source_data_type=column.get("data_type"),
            task=task,
            position=i,
        )

        if BigQueryDataType.objects.filter(
            name=DATA_TYPE_MAPPING.get(column.get("data_type", "").upper())
        ).exists():
            field.data_type = BigQueryDataType.objects.filter(
                name=DATA_TYPE_MAPPING.get(column.get("data_type"))
            )[0]

        if field.data_type.name != DATA_TYPE_MAPPING.get(
            column.get("data_type", "").upper()
        ):
            field.transformation = f"safe_cast({column.get('column_name')} as {field.data_type.name.lower()})"
            column["transformation"] = True
        else:
            column["transformation"] = False

        field.save()
        column["id"] = field.id
        column["data_type"] = field.data_type.name
        column["position"] = i

    return response.Response(data=table, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def datatypecomparison(
    request: request, source: str, target: str, column: str
) -> response.Response:
    """
    If the target data type is different from the source data type, and the target data type exists in
    the database, then return the column name casted to the target data type

    Args:
      request (request): The request object.
      source (str): The data type of the column in the source table.
      target (str): The target data type
      column (str): The column name that you want to cast.

    Returns:
      A response object with the data and status code.
    """
    data = None

    if (
        target != DATA_TYPE_MAPPING.get(source.upper())
        and BigQueryDataType.objects.filter(name=target).exists()
    ):
        data = f"safe_cast({column} as {target.lower()})"

    return response.Response(data=data, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def fieldpositionchange(
    request: request, task_id: int, field_id: int, position: int
) -> response.Response:
    """
    > Change the position of a field in a task

    Args:
      request (request): request - This is the request object that is passed to the view.
      task_id (int): The id of the task that the field belongs to.
      field_id (int): The id of the field you want to change the position of.
      position (int): The position of the field in the task.

    Returns:
      A response object with the data and status code.
    """
    field = Field.objects.get(id=field_id)
    if field.position == position:
        return response.Response(data=None, status=status.HTTP_304_NOT_MODIFIED)
    changefieldposition(field, field.position, position)
    field.position = position
    field.save()

    return response.Response(data=None, status=status.HTTP_200_OK)
