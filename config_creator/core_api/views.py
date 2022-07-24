import re

from copy import deepcopy
from core.forms import FieldForm, JoinForm
from core.models import (
    BigQueryDataType,
    changefieldposition,
    changeorderposition,
    Condition,
    DATA_TYPE_MAPPING,
    DEFAULT_DATA_TYPE_ID,
    DrivingColumn,
    Field,
    History,
    HistoryOrder,
    Job,
    JobTask,
    Join,
    Partition,
    SourceTable,
    str_to_class,
    get_source_table,
)
from database_interface_api.dbhelper import get_table
from database_interface_api.views import get_connection
from django import views
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import renderers, response, request, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

__all__ = [
    "FieldView",
    "copytable",
    "datatypecomparison",
    "datatypemap",
    "fieldpositionchange",
    "JobView",
    "ConditionView",
    "SourceTableView",
    "DrivingColumnView",
    "PartitionView",
    "HistoryOrderView",
]


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

        field = (
            Field.objects.get(id=pk) if Field.objects.filter(id=pk).exists() else None
        )
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

    def get(self, request: request, pk: int) -> response.Response:
        field = (
            Field.objects.get(id=pk) if Field.objects.filter(id=pk).exists() else None
        )
        if field:
            outp = field.todict()
            return_status = status.HTTP_200_OK
        else:
            outp = {}
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data={"result": outp}, status=return_status)

    def post(self, request: request, task_id: int, pk: int = None) -> response.Response:

        action = request.POST.get("action")
        data = {}
        return_status = None
        if action:
            if action in ["createColumn", "editColumn"]:
                m = re.search(
                    r"^(?P<dataset_name>\w+)\.(?P<table_name>\w+)(?:\s(?P<alias>\w+))?",
                    request.POST.get("source_name", ""),
                    re.IGNORECASE,
                )
                source_table = get_source_table(
                    task_id,
                    m.group("dataset_name"),
                    m.group("table_name"),
                    m.group("alias"),
                )
                request_post = deepcopy(request.POST)
                request_post["source_table"] = source_table.id
                form = FieldForm(request_post)
                if pk:
                    form.instance.id = pk
                message = (
                    f"{request.POST.get('name', 'Field')} updated."
                    if pk
                    else f"{request.POST.get('name', 'Field')} created."
                )
                form.instance.task_id = task_id
                if form.is_valid():
                    form.save()
                    data = {
                        "message": message,
                        "type": "Success",
                        "result": {
                            "content": [
                                Field.objects.get(id=form.instance.id).todict()
                            ],
                        },
                    }

                    return_status = status.HTTP_200_OK
                else:
                    return_status = status.HTTP_400_BAD_REQUEST

            elif action in [
                "createDrivingColumn",
                "createPartition",
                "createHistoryOrder",
            ]:
                class_type = re.sub(r"^(create)", "", action)
                column_class = str_to_class(class_type)
                history = History.objects.get(task_id=task_id)
                if column_class:
                    column = column_class(history_id=history.id)
                    column.position = (
                        len(column_class.objects.filter(history_id=history.id)) + 1
                    )

                    field_name = (
                        request.POST.get("name", "Field")
                        if request.POST.get("name", "Field") != ""
                        else "Field"
                    )
                    field_type = re.sub(r"^([A-Z].+)([A-Z])", r"\1 \2", class_type)

                    if Field.objects.filter(
                        source_name=request.POST.get("source_name"),
                        source_column=request.POST.get("source_column"),
                        is_source_to_target=True,
                    ).exists():
                        field = Field.objects.get(
                            source_name=request.POST.get("source_name"),
                            source_column=request.POST.get("source_column"),
                            is_source_to_target=True,
                        )
                        if action == "createPartition":
                            field.is_history_key = True
                        field.save()
                        field_id = field.id

                        message = f"{field_type} {field_name} updated."

                    else:
                        form = FieldForm(request.POST)
                        message = f"{field_type} {field_name} created."

                        form.instance.task_id = task_id
                        form.instance.position = -1
                        form.instance.data_type = BigQueryDataType.objects.get(
                            id=DEFAULT_DATA_TYPE_ID
                        )
                        form.instance.is_source_to_target = False
                        if form.is_valid():
                            form.save()
                            field_id = form.instance.id
                        else:
                            return_status = status.HTTP_400_BAD_REQUEST

                    if not return_status:
                        data = {
                            "message": message,
                            "type": "Success",
                        }
                        column.field_id = field_id

                        column.save()
                        data["result"] = {
                            "content": [Field.objects.get(id=column.field_id).todict()],
                        }
                        data["result"]["content"][0]["position"] = column.position

                        return_status = status.HTTP_200_OK
                else:

                    data = {
                        "message": "Incorrect action supplied",
                        "type": "Error",
                    }
                    return_status = status.HTTP_400_BAD_REQUEST

        else:
            data = {
                "message": f"No action provided.",
                "type": "error",
            }
            return_status = status.HTTP_400_BAD_REQUEST

        return response.Response(data=data, status=return_status)


class JoinView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request: request, pk: int) -> response.Response:

        join = Join.objects.get(id=pk) if Join.objects.filter(id=pk).exists() else None
        if join:
            outp = {
                "message": f"Join '{join.name}' deleted.",
                "type": "success",
            }
            join.delete()
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Join with id '{pk}' does not exist.",
                "type": "error",
            }
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data=outp, status=return_status)

    def get(self, request: request, pk: int) -> response.Response:
        join = Join.objects.get(id=pk) if Join.objects.filter(id=pk).exists() else None
        if join:
            outp = join.todict()
            return_status = status.HTTP_200_OK
        else:
            outp = {}
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data={"result": outp}, status=return_status)

    def post(self, request: request, task_id: int, pk: int = None) -> response.Response:

        task = JobTask.objects.get(id=task_id)
        m = re.search(
            r"^(?P<dataset_name>\w+)\.(?P<table_name>\w+)(?:\s(?P<alias>\w+))?",
            request.POST.get("left", task.driving_table),
            re.IGNORECASE,
        )

        left_table = get_source_table(
            task_id,
            m.group("dataset_name"),
            m.group("table_name"),
            m.group("alias"),
        )

        m = re.search(
            r"^(?P<dataset_name>\w+)\.(?P<table_name>\w+)(?:\s(?P<alias>\w+))?",
            request.POST.get("right", ""),
            re.IGNORECASE,
        )

        right_table = get_source_table(
            task_id,
            m.group("dataset_name"),
            m.group("table_name"),
            m.group("alias"),
        )

        request_post = deepcopy(request.POST)
        request_post["left_table"] = left_table.id
        request_post["right_table"] = right_table.id
        form = JoinForm(request_post)
        if pk:
            form.instance.id = pk
        message = "Join updated." if pk else "Join created."
        form.instance.task_id = task_id
        if form.is_valid():
            form.save()
            data = {
                "message": message,
                "type": "Success",
                "result": {
                    "content": [Join.objects.get(id=form.instance.id).todict()],
                },
            }

            return_status = status.HTTP_200_OK
        else:
            return_status = status.HTTP_400_BAD_REQUEST

        return response.Response(data={"result": data}, status=return_status)


class DrivingColumnView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request: request, pk: int) -> response.Response:

        driving_column = (
            DrivingColumn.objects.get(id=pk)
            if DrivingColumn.objects.filter(id=pk).exists()
            else None
        )
        if driving_column:
            outp = {
                "message": f"Driving Column deleted.",
                "type": "success",
            }

            field = Field.objects.get(
                id=driving_column.field_id,
            )
            if (
                not DrivingColumn.objects.filter(
                    ~Q(id=driving_column.id),
                    field_id=field.id,
                ).exists()
                and not field.is_source_to_target
                and not Partition.objects.filter(
                    field_id=field.id,
                ).exists()
                and not HistoryOrder.objects.filter(
                    field_id=field.id,
                ).exists()
                and not Condition.objects.filter(
                    left_id=field.id,
                ).exists()
                and not Condition.objects.filter(
                    right_id=field.id,
                ).exists()
            ):
                field.delete()

            driving_column.delete()
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Driving column with id '{pk}' does not exist.",
                "type": "error",
            }
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data=outp, status=return_status)


class PartitionView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request: request, pk: int) -> response.Response:

        partition = (
            Partition.objects.get(id=pk)
            if Partition.objects.filter(id=pk).exists()
            else None
        )
        if partition:
            outp = {
                "message": f"Partition column deleted.",
                "type": "success",
            }

            field = Field.objects.get(
                id=partition.field_id,
            )
            if (
                not DrivingColumn.objects.filter(
                    field_id=field.id,
                ).exists()
                and not field.is_source_to_target
                and not Partition.objects.filter(
                    ~Q(id=partition.id),
                    field_id=field.id,
                ).exists()
                and not HistoryOrder.objects.filter(
                    field_id=field.id,
                ).exists()
                and not Condition.objects.filter(
                    left_id=field.id,
                ).exists()
                and not Condition.objects.filter(
                    right_id=field.id,
                ).exists()
            ):
                field.delete()
            elif (
                field.is_source_to_target
                and not Partition.objects.filter(
                    ~Q(id=partition.id),
                    field_id=field.id,
                ).exists()
            ):
                field.is_history_key = False
                field.save()

            partition.delete()
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Partition column with id '{pk}' does not exist.",
                "type": "error",
            }
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data=outp, status=return_status)


class HistoryOrderView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request: request, pk: int) -> response.Response:

        history_order = (
            HistoryOrder.objects.get(id=pk)
            if HistoryOrder.objects.filter(id=pk).exists()
            else None
        )

        if history_order:
            outp = {
                "message": f"Order column deleted.",
                "type": "success",
            }

            field = Field.objects.get(
                id=history_order.field_id,
            )

            if (
                not DrivingColumn.objects.filter(
                    field_id=field.id,
                ).exists()
                and not field.is_source_to_target
                and not Partition.objects.filter(
                    field_id=field.id,
                ).exists()
                and not HistoryOrder.objects.filter(
                    ~Q(id=history_order.id),
                    field_id=field.id,
                ).exists()
                and not Condition.objects.filter(
                    left_id=field.id,
                ).exists()
                and not Condition.objects.filter(
                    right_id=field.id,
                ).exists()
            ):
                field.delete()

            history_order.delete()
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Order column with id '{pk}' does not exist.",
                "type": "error",
            }
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data=outp, status=return_status)


class JobView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request: request, pk: int) -> response.Response:

        job = Job.objects.get(id=pk)
        if job:
            outp = {
                "message": f"Job '{job.name}' deleted.",
                "type": "success",
            }
            job.delete()
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Job with id '{pk}' does not exist.",
                "type": "error",
            }
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data=outp, status=return_status)


class ConditionView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request: request, pk: int) -> response.Response:

        condition = Condition.objects.get(id=pk)
        if condition:
            outp = {
                "message": f"Condition deleted.",
                "type": "success",
            }
            condition.delete()
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Condition with id '{pk}' does not exist.",
                "type": "error",
            }
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data=outp, status=return_status)


class SourceTableView(views.APIView):

    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request: request, pk: int) -> response.Response:

        source_table = SourceTable.objects.filter(id=pk).exists()
        if source_table:
            source_table = SourceTable.objects.get(id=pk)
            outp = {
                "result": source_table,
            }
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Source Table with id '{pk}' does not exist.",
                "type": "error",
            }
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data=outp, status=return_status)

    def post(self, request: request, pk: int) -> response.Response:

        source_table = SourceTable.objects.filter(id=pk).exists()
        if source_table:
            source_table = SourceTable.objects.get(id=pk)
            source_table.source_project = request.POST.get("source_project")
            source_table.save()
            outp = {
                "message": f"Source Table updated.",
                "type": "success",
            }
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Source Table with id '{pk}' does not exist.",
                "type": "error",
            }
            return_status = status.HTTP_404_NOT_FOUND

        return response.Response(data=outp, status=return_status)

    def delete(self, request: request, pk: int) -> response.Response:

        source_table = SourceTable.objects.filter(id=pk).exists()
        if source_table:
            source_table = SourceTable.objects.get(id=pk)
            outp = {
                "message": f"Source Table deleted.",
                "type": "success",
            }
            source_table.delete()
            return_status = status.HTTP_200_OK
        else:
            outp = {
                "message": f"Source Table with id '{pk}' does not exist.",
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


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def datatypemap(request: request, source: str) -> response.Response:

    return response.Response(
        data=DATA_TYPE_MAPPING.get(source.upper()), status=status.HTTP_200_OK
    )


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


@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def orderpositionchange(
    request: request, task_id: int, order_id: int, position: int
) -> response.Response:
    order = HistoryOrder.objects.get(id=order_id)
    if order.position == position:
        return response.Response(data=None, status=status.HTTP_304_NOT_MODIFIED)
    changeorderposition(order, order.position, position)
    order.position = position
    order.save()

    return response.Response(data=None, status=status.HTTP_200_OK)
