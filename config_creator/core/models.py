import re
import sys

from django.db import models
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from wordsegment import segment

__all__ = [
    "JobType",
    "TaskType",
    "TableType",
    "WriteDisposition",
    "LogicOperator",
    "Operator",
    "JoinType",
    "JobToTaskType",
    "Job",
    "JobTask",
    "History",
    "Field",
    "Dependency",
    "DrivingColumn",
    "Partition",
    "HistoryOrder",
    "Delta",
    "Join",
    "Condition",
    "BatchJobProperties",
    "DEFAULT_TASK_ID",
    "DEFAULT_TABLE_ID",
    "DEFAULT_WRITE_DISPOSITION_ID",
    "DEFAULT_LOGIC_OPERATOR_ID",
    "DEFAULT_OPERATOR_ID",
    "DEFAULT_JOIN_ID",
    "DagJobProperties",
    "BatchCustomJobTaskProperties",
    "BigQueryDataType",
    "DATA_TYPE_MAPPING",
    "changefieldposition",
    "DEFAULT_DATA_TYPE_ID",
    "SourceTable",
    "changeorderposition",
    "get_source_table",
]

User = settings.AUTH_USER_MODEL

DATA_TYPE_MAPPING = {
    "CHAR": "STRING",
    "VARCHAR": "STRING",
    "VARCHAR2": "STRING",
    "DATE": "DATE",
    "TIMESTAMP": "TIMESTAMP",
    "BYTEINT": "INT64",
    "SMALLINT": "INT64",
    "INTEGER": "INT64",
    "BIGINT": "INT64",
    "NUMBER": "NUMERIC",
    "NUMERIC": "NUMERIC",
    "DECIMAL": "NUMERIC",
    "BINARY DOUBLE": "FLOAT64",
    "DOUBLE PRECISION": "FLOAT64",
    "BINARY FLOAT": "FLOAT64",
    "DOUBLE": "FLOAT64",
    "BOOL": "BOOL",
    "STRING": "STRING",
    "FLOAT64": "FLOAT64",
    "INT64": "INT64",
}

DEFAULT_ID = 1
DEFAULT_TASK_ID = DEFAULT_ID
DEFAULT_TABLE_ID = DEFAULT_ID
DEFAULT_WRITE_DISPOSITION_ID = DEFAULT_ID
DEFAULT_LOGIC_OPERATOR_ID = DEFAULT_ID
DEFAULT_OPERATOR_ID = DEFAULT_ID
DEFAULT_JOIN_ID = DEFAULT_ID
DEFAULT_DATA_TYPE_ID = DEFAULT_ID


class JobType(models.Model):
    name = models.CharField(
        verbose_name="Job Type",
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    code = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(
        verbose_name="Task Type",
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    code = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TableType(models.Model):
    name = models.CharField(
        verbose_name="Table Type",
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    code = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class WriteDisposition(models.Model):
    name = models.CharField(
        verbose_name="Write Disposition",
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    code = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class LogicOperator(models.Model):
    name = models.CharField(
        verbose_name="Logic Operator",
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    code = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Operator(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    code = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    symbol = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class JoinType(models.Model):
    name = models.CharField(
        verbose_name="Join Type",
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    code = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class JobToTaskType(models.Model):
    jobtype = models.ForeignKey(JobType, null=False, on_delete=models.CASCADE)
    tasktype = models.ForeignKey(TaskType, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.jobtype.name}: {self.tasktype.name}"


class Job(models.Model):
    name = models.SlugField(
        verbose_name="Job Name",
        max_length=255,
        blank=False,
        null=False,
        unique=False,
    )
    type = models.ForeignKey(JobType, on_delete=models.SET_NULL, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    properties = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="job_created_by"
    )
    lastupdate = models.DateTimeField(auto_now=True)
    updatedby = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="job_updated_by"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        It returns the URL of the job detail page for the job with the primary key of self.id.

        Returns:
          The url for the job-change page.
        """
        return reverse("job-change", kwargs={"pk": self.id})

    def get_property_object(self):
        """
        It takes a job object, and returns the job's properties object

        Returns:
          The property object for the job.
        """
        property_class = str_to_class(f"{self.type.code.title()}JobProperties")
        if property_class:
            if property_class.objects.filter(job_id=self.id).exists():
                return property_class.objects.get(
                    job_id=self.id,
                )
            else:
                return property_class(
                    job_id=self.id,
                )

        return None

    def todict(self):
        return {
            "name": self.name,
            "type": self.type.name,
            "description": self.description,
            "properties": self.get_property_object().todict()
            if self.get_property_object()
            else None,
            "created": self.created,
            "createdby": self.createdby.get_full_name(),
            "lastupdate": self.lastupdate,
            "updatedby": self.updatedby.get_full_name(),
        }


class JobTask(models.Model):
    name = models.SlugField(
        verbose_name="Task Name",
        max_length=255,
        blank=False,
        null=False,
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=False, null=False)
    type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_DEFAULT,
        blank=False,
        null=False,
        default=DEFAULT_TASK_ID,
        verbose_name="Task Type",
        help_text="Select task type.",
    )
    table_type = models.ForeignKey(
        TableType,
        on_delete=models.SET_DEFAULT,
        blank=False,
        null=False,
        default=DEFAULT_TABLE_ID,
        verbose_name="Target Table Type",
        help_text="Select desired SCD table type.",
    )
    write_disposition = models.ForeignKey(
        WriteDisposition,
        on_delete=models.SET_DEFAULT,
        blank=False,
        null=False,
        default=DEFAULT_WRITE_DISPOSITION_ID,
        verbose_name="Write Disposition",
        help_text="Select type of update to be performed on target table.",
    )
    destination_table = models.CharField(
        verbose_name="Destination Table",
        max_length=255,
        blank=False,
        null=False,
        help_text="Enter the destination table name.",
    )
    destination_dataset = models.CharField(
        verbose_name="Destination Dataset",
        max_length=255,
        blank=True,
        null=True,
        help_text="Enter the dataset containing the target table.",
    )
    driving_table = models.CharField(
        verbose_name="Driving Table",
        max_length=255,
        blank=True,
        null=True,
        help_text="Enter the driving table and dataset in format: <driving dataset name>.<driving table name>",
    )
    staging_dataset = models.CharField(
        verbose_name="Staging Dataset",
        max_length=255,
        blank=True,
        null=True,
        help_text="Enter a staging dataset to be used for any pre-processing, can be left blank to default to Job value.",
    )
    properties = models.JSONField(
        blank=True,
        null=True,
        help_text="Enter additional task properties in JSON format.",
    )
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="job_task_created_by"
    )
    lastupdate = models.DateTimeField(auto_now=True)
    updatedby = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="job_task_updated_by"
    )

    def __str__(self):
        return self.name

    def get_property_object(self):

        """
        It takes a task object, and returns the corresponding property object

        Returns:
          The property object for the task.
        """
        property_class = str_to_class(
            f"{self.job.type.code.title()}{self.type.code.title()}JobTaskProperties"
        )
        if property_class:
            if property_class.objects.filter(task_id=self.id).exists():
                return property_class.objects.get(
                    task_id=self.id,
                )
            else:
                return property_class(
                    task_id=self.id,
                )

        return None

    def todict(self):
        return {
            "name": self.name,
            "job": self.job.todict(),
            "type": self.type.name,
            "table_type": self.table_type.name,
            "write_disposition": self.write_disposition.name,
            "destination_dataset": self.destination_dataset,
            "destination_table": self.destination_table,
            "driving_table": self.driving_table,
            "staging_dataset": self.staging_dataset,
            "description": self.description,
            "properties": self.get_property_object().todict()
            if self.get_property_object()
            else None,
            "created": self.created,
            "createdby": self.createdby.get_full_name(),
            "lastupdate": self.lastupdate,
            "updatedby": self.updatedby.get_full_name(),
        }


class History(models.Model):
    class Meta:
        verbose_name = "Historie"

    task = models.OneToOneField(
        JobTask, on_delete=models.CASCADE, blank=False, null=False
    )

    def __str__(self):
        return f"{self.task.name} history"


class BigQueryDataType(models.Model):
    name = models.CharField(
        verbose_name="Data Type",
        max_length=255,
        blank=False,
        null=False,
        help_text="",
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SourceTable(models.Model):
    task = models.ForeignKey(JobTask, on_delete=models.CASCADE, blank=False, null=False)
    source_project = models.CharField(
        verbose_name="Source Project",
        max_length=255,
        blank=True,
        null=True,
    )
    dataset_name = models.CharField(
        verbose_name="Dataset Name",
        max_length=255,
        blank=False,
        null=False,
    )
    table_name = models.CharField(
        verbose_name="Table Name",
        max_length=255,
        blank=False,
        null=False,
    )
    alias = models.CharField(
        verbose_name="Table Alias",
        max_length=255,
        blank=True,
        null=False,
        unique=False,
    )
    base_alias = models.CharField(
        verbose_name="Base Table Alias",
        max_length=255,
        blank=True,
        null=False,
        unique=False,
        help_text="Non-unique alias, used to identify number of occurences of the table.",
    )

    def save(self, *args, **kwargs):
        if self.source_project is None:
            job_properties = Job.objects.get(
                id=JobTask.objects.get(id=self.task_id).job_id
            ).get_property_object()
            if job_properties:
                self.source_project = job_properties.source_project

        if self.id is None:
            cleaned_table_name = re.sub(
                r"^((?:cc|fc)_[a-z]+_)", "", self.table_name.lower()
            )

            if self.alias:
                alias = self.alias
            else:
                alias = "".join([w[:1] for w in segment(cleaned_table_name)])
                m = re.search(r"_(p\d+)$", cleaned_table_name, re.IGNORECASE)
                if m:
                    alias = m.group(1)

            tables = SourceTable.objects.filter(
                base_alias=alias,
                task_id=self.task_id,
            )

            if tables.exists():
                counter = len(tables) + 1
                self.alias = f"{alias}_{counter}"
            else:
                self.alias = alias

            self.base_alias = alias

        super(SourceTable, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.dataset_name}.{self.table_name} {self.alias}"

    def todict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "source_project": self.source_project,
            "dataset_name": self.dataset_name,
            "table_name": self.table_name,
            "alias": self.alias,
        }


def get_source_table(
    task_id: int, dataset_name: str, table_name: str, alias: str = None
) -> SourceTable:
    """
    > If a SourceTable object exists with the given task_id, dataset_name, table_name, and alias, return
    it. Otherwise, create a new SourceTable object with the given task_id, dataset_name, and table_name,
    and return it

    Args:
      task_id (int): The id of the task that the source table is associated with.
      dataset_name (str): The name of the dataset that the table is in.
      table_name (str): The name of the table in the dataset.
      alias (str): The alias of the table.

    Returns:
      A SourceTable object
    """
    if dataset_name is None or table_name is None:
        return None

    if SourceTable.objects.filter(
        task_id=task_id,
        dataset_name=dataset_name,
        table_name=table_name,
        alias=alias,
    ).exists():
        return SourceTable.objects.get(
            task_id=task_id,
            dataset_name=dataset_name,
            table_name=table_name,
            alias=alias,
        )
    else:
        saved = SourceTable(
            task_id=task_id,
            dataset_name=dataset_name,
            table_name=table_name,
            alias=alias,
        )
        saved.save()
        return saved


class Field(models.Model):
    name = models.CharField(
        verbose_name="Name", max_length=255, blank=True, null=True, help_text=""
    )
    data_type = models.ForeignKey(
        BigQueryDataType,
        verbose_name="Data Type",
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_DATA_TYPE_ID,
        null=False,
        blank=True,
    )
    position = models.IntegerField(
        verbose_name="Ordinal Position",
        null=False,
        blank=True,
        default=-1,
        help_text="Enter the column's position within the target table",
    )
    source_column = models.CharField(
        verbose_name="Source Column",
        max_length=255,
        blank=True,
        null=True,
        help_text="",
    )
    source_table = models.ForeignKey(
        SourceTable,
        verbose_name="Source Table",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Source for the column, include dataset and table names: <dataset name>.<table name>",
    )
    source_data_type = models.CharField(
        verbose_name="Source Data Type",
        max_length=255,
        blank=True,
        null=True,
        help_text="Data type for the column at source",
    )
    transformation = models.TextField(
        verbose_name="Column Transformation",
        blank=True,
        null=True,
        help_text="",
    )
    is_source_to_target = models.BooleanField(default=True)
    is_primary_key = models.BooleanField(
        verbose_name="Primary Key Field",
        default=False,
        help_text="Indictes the field is part of the table key.",
    )
    is_history_key = models.BooleanField(
        verbose_name="History Key Field", default=False
    )
    is_nullable = models.BooleanField(verbose_name="Is Column Nullable", default=True)
    task = models.ForeignKey(JobTask, on_delete=models.CASCADE, null=False)

    def __str__(self):
        """
        If the column has a transformation, return the transformation and the name. If the column has a
        source table and column, return the source table and column and the name. If the column has a
        source table and no column, return the source table and the name. If the column has no source
        table, return the name

        Returns:
          The name of the column, the table it is in, and the dataset it is in.
        """
        name = ""
        table = ""
        column = ""

        if self.transformation:
            if self.name:
                name = f" as {self.name}"

            return f"{self.transformation}{name}"

        if self.source_table:
            table = f"{self.source_table.dataset_name}.{self.source_table.table_name}."

        if self.source_column:
            column = f"{self.source_column}"
            if self.name:
                name = f" as {self.name}"
        else:
            name = f"{self.name}"

        return f"{table}{column}{name}"

    def todict(self) -> dict:
        """
        It takes a column object and returns a dictionary with the column's name, data type, source
        name, source column, source data type, transformation, position, is_primary_key, is_nullable,
        and id

        Returns:
          A dictionary with the column name, data type, source name, source column, source data type,
        transformation, position, is primary key, is nullable, and id.
        """
        outp = {
            "name": self.name,
            "data_type": self.data_type.name if self.data_type else None,
            "data_type_id": self.data_type_id,
            "source_name": f"{self.source_table.dataset_name}.{self.source_table.table_name}"
            if self.source_table
            else None,
            "source_table_alias": self.source_table.alias
            if self.source_table
            else None,
            "source_table": self.source_table.todict() if self.source_table else None,
            "source_column": self.source_column,
            "source_data_type": self.source_data_type,
            "transformation": self.transformation,
            "position": self.position,
            "is_primary_key": self.is_primary_key,
            "is_nullable": self.is_nullable,
            "is_history_key": self.is_history_key,
            "id": self.id,
        }

        if self.source_table:
            outp["source_name"] = (
                f"{self.source_table.dataset_name}.{self.source_table.table_name}"
                if self.source_table.dataset_name and self.source_table.table_name
                else None
            )

        return outp


def changefieldposition(field: Field, original_position: int, position: int) -> int:
    """
    If the field's position is changed, then re-order all fields in the task

    Args:
      field (Field): Field = the field object that is being re-ordered
      original_position (int): the original position of the field
      position (int): the new position of the field

    Returns:
      0
    """
    if original_position != position:
        fields = Field.objects.filter(
            ~Q(id=field.id), task_id=field.task_id, is_source_to_target=True
        ).order_by("position")
        max_field_position = len(fields) + 1
        if original_position > max_field_position:
            original_position = max_field_position
        if fields.exists():
            for i, f in enumerate(fields):
                # identify what the current position iterator position is
                if i + 1 >= position:
                    current_position = i + 2
                else:
                    current_position = i + 1

                f.position = current_position

                f.save()
    return 0


class Dependency(models.Model):
    class Meta:
        verbose_name = "Dependencie"

    predecessor = models.ForeignKey(
        JobTask, on_delete=models.CASCADE, null=False, related_name="predecessor"
    )
    dependant = models.ForeignKey(
        JobTask, on_delete=models.CASCADE, null=False, related_name="dependant"
    )

    def todict(self):
        return {
            "predecessor": self.predecessor.todict(),
            "dependant": self.dependant.todict(),
        }


class DrivingColumn(models.Model):
    history = models.ForeignKey(
        History, on_delete=models.CASCADE, blank=False, null=False
    )
    position = models.IntegerField(null=False)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"Driving Column - {self.position}"


class Partition(models.Model):
    history = models.ForeignKey(
        History, on_delete=models.CASCADE, blank=False, null=False
    )
    position = models.IntegerField(null=False)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"Partition Column - {self.position}"


class HistoryOrder(models.Model):
    history = models.ForeignKey(
        History,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    position = models.IntegerField(
        null=False,
    )
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        null=False,
    )
    is_desc = models.BooleanField(
        verbose_name="Is Descending?",
        default=False,
        blank=True,
        null=False,
    )

    def __str__(self):
        return f"Order By - {self.position}"


def changeorderposition(
    history_order: HistoryOrder, original_position: int, position: int
) -> int:
    """
    If the original position of the order is not the same as the new position, then get all the orders
    for the task, order them by position, and then loop through them, updating the position of each
    order to be one less than the original position if the original position is greater than the new
    position, and one more than the original position if the original position is less than the new
    position

    Args:
      history_order (HistoryOrder): HistoryOrder, original_position: int, position: int
      original_position (int): the original position of the order
      position (int): the new position of the order

    Returns:
      0
    """
    if original_position != position:
        orders = HistoryOrder.objects.filter(
            ~Q(id=history_order.id), task_id=history_order.task_id
        ).order_by("position")
        max_field_position = len(orders) + 1
        if original_position > max_field_position:
            original_position = max_field_position
        if orders.exists():
            for i, f in enumerate(orders):
                # if field has default position (-1), or 0 position then set it to
                # the field's index in returned queryset
                if f.position < 1:
                    f.position = i + 1

                # if field's position is greater than total number of fields, this can stop
                # re-order.  so set it to total number of fields
                if f.position > max_field_position:
                    f.position = max_field_position

                if (
                    f.position <= position
                    and f.position > 0
                    and f.position > original_position
                    and original_position > 0
                ):
                    f.position = f.position - 1
                elif (
                    f.position > position
                    and f.position > 0
                    and f.position < original_position
                    and original_position > 0
                ):
                    f.position = f.position + 1

                f.save()
    return 0


class Delta(models.Model):
    task = models.OneToOneField(
        JobTask, on_delete=models.CASCADE, blank=False, null=False
    )
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=False)
    lower_bound = models.CharField(
        verbose_name="Lower Bound",
        max_length=255,
        blank=False,
        null=False,
        help_text="""Input a function that returns a date value or use preset;
$YESTERDAY = today's date minus one day
    $TODAY = today's date
 $THISWEEK = start date of current week, start date = MONDAY
$THISMONTH = date of first day of current month
""",
    )
    upper_bound = models.IntegerField(
        blank=True,
        null=True,
        help_text="Input seconds to add to lower_bound, 86400 represents one day",
    )

    def todict(self):
        return {
            "id": self.id,
            "task_id": self.task.id,
            "lower_bound": self.lower_bound,
            "upper_bound": self.upper_bound,
            "field": self.field.todict(),
        }


class Join(models.Model):
    left_table = models.ForeignKey(
        SourceTable,
        verbose_name="Left Table",
        on_delete=models.CASCADE,
        null=False,
        blank=True,
        related_name="left_table",
    )
    right_table = models.ForeignKey(
        SourceTable,
        verbose_name="Right Table",
        on_delete=models.CASCADE,
        null=False,
        blank=True,
        related_name="right_table",
    )
    type = models.ForeignKey(
        JoinType, on_delete=models.SET_DEFAULT, null=False, default=DEFAULT_JOIN_ID
    )
    task = models.ForeignKey(JobTask, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        """
        The function returns a string that contains the name of the task and the name of the right table

        Returns:
          The name of the task and the right table it is joining to.
        """
        return f"{self.task.name}: join to {self.right_table}"

    def todict(self):
        """
        It returns a dictionary of the object's attributes

        Returns:
          A dictionary of the join object.
        """
        return {
            "id": self.id,
            "type": self.type.name,
            "left_table": self.left_table.__str__(),
            "right_table": self.right_table.__str__(),
            "conditions": [
                condition.todict()
                for condition in Condition.objects.filter(join_id=self.id)
            ],
            "task_id": self.task_id,
        }


class Condition(models.Model):
    operator = models.ForeignKey(
        Operator,
        on_delete=models.SET_DEFAULT,
        blank=False,
        null=False,
        default=DEFAULT_OPERATOR_ID,
    )
    logic_operator = models.ForeignKey(
        LogicOperator,
        on_delete=models.SET_DEFAULT,
        blank=False,
        null=False,
        default=DEFAULT_LOGIC_OPERATOR_ID,
    )
    join = models.ForeignKey(
        Join,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    where = models.ForeignKey(
        JobTask,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    left = models.ForeignKey(
        Field,
        verbose_name="Left Parameter",
        null=True,
        blank=True,
        max_length=255,
        related_name="left_parameter",
        on_delete=models.CASCADE,
    )
    right = models.ForeignKey(
        Field,
        verbose_name="Right Parameter",
        null=True,
        blank=True,
        max_length=255,
        related_name="right_parameter",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.join.task.name if self.join else (self.where.name if self.where else '')}{'Join Condition' if self.join else ('Where Condition' if self.where else '')}"

    def todict(self):
        return {
            "id": self.id,
            "operator": self.operator.name,
            "logic_operator": self.logic_operator.name,
            "left": self.left.todict(),
            "right": self.right.todict(),
        }


class BaseJobProperties(models.Model):
    job = models.OneToOneField(
        to=Job,
        on_delete=models.CASCADE,
        unique=True,
    )
    dataset_source = models.CharField(
        verbose_name="Source Dataset",
        max_length=255,
        unique=False,
        blank=False,
        null=False,
        help_text="default value for all tasks in this job",
    )
    dataset_staging = models.CharField(
        verbose_name="Staging Dataset",
        max_length=255,
        unique=False,
        blank=False,
        null=False,
        help_text="Default value for all tasks in this job",
    )
    dataset_publish = models.CharField(
        verbose_name="Target Dataset",
        max_length=255,
        unique=False,
        blank=False,
        null=False,
        help_text="Default value for all tasks in this job",
    )
    source_project = models.CharField(
        verbose_name="Source Project",
        max_length=255,
        blank=True,
        null=True,
        help_text="Default source project",
    )
    target_project = models.CharField(
        verbose_name="Target Project",
        max_length=255,
        blank=True,
        null=True,
        help_text="Target project",
    )

    class Meta:
        abstract = True

    def todict(self):
        return {
            "dataset_source": self.dataset_source,
            "dataset_publish": self.dataset_publish,
            "dataset_staging": self.dataset_staging,
            "target_project": self.target_project,
            "source_project": self.source_project,
        }


class BatchJobProperties(BaseJobProperties):
    prefix = models.CharField(
        verbose_name="Script Name Prefix",
        max_length=255,
        unique=False,
        blank=False,
        null=False,
        help_text="Enter the prefix which will be used for all tasks in this job; i.e. spine_order",
    )

    def todict(self):
        return {
            "dataset_source": self.dataset_source,
            "dataset_publish": self.dataset_publish,
            "dataset_staging": self.dataset_staging,
            "target_project": self.target_project,
            "source_project": self.source_project,
            "prefix": self.prefix,
        }


class DagJobProperties(BaseJobProperties):
    tags = models.CharField(
        verbose_name="Job Tags",
        max_length=255,
        unique=False,
        blank=True,
        null=True,
        help_text="Enter tags for the job, seperated by a semi-colon ';'",
    )
    owner = models.CharField(
        verbose_name="Job Owner",
        max_length=255,
        unique=False,
        blank=False,
        null=False,
    )
    email = models.CharField(
        verbose_name="Email",
        max_length=255,
        unique=False,
        blank=True,
        null=True,
        help_text="Enter email address for the job to contact, seperated by a semi-colon ';'",
    )
    imports = models.CharField(
        verbose_name="Imports",
        max_length=255,
        unique=False,
        blank=True,
        null=True,
        help_text="Enter any python packages to be imported, seperated by a semi-colon ';'",
    )

    def todict(self):
        return {
            "dataset_source": self.dataset_source,
            "dataset_publish": self.dataset_publish,
            "dataset_staging": self.dataset_staging,
            "target_project": self.target_project,
            "source_project": self.source_project,
            "tags": self.tags,
            "owner": self.owner,
            "email": self.email,
            "imports": self.imports,
        }


class BaseJobTaskProperties(models.Model):
    task = models.OneToOneField(
        to=JobTask,
        on_delete=models.CASCADE,
        unique=True,
    )

    class Meta:
        abstract = True

    def todict(self):
        return {}


class BatchCustomJobTaskProperties(BaseJobTaskProperties):
    sql = models.CharField(
        verbose_name="Sql Script Name",
        max_length=255,
        unique=False,
        blank=False,
        null=False,
        help_text="Enter the name of the sql fiel to be used by this task",
    )

    def todict(self):
        return {"sql": self.sql}


def str_to_class(classname):
    """
    It takes a string and returns the class object that the string represents

    Args:
      classname: The name of the class you want to instantiate.

    Returns:
      The class object of the classname string.
    """
    try:
        return getattr(sys.modules[__name__], classname)
    except AttributeError:
        return None
