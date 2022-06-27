from asyncio import Task
from tkinter import CASCADE
from turtle import position
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

DEFAULT_ID = 1
DEFAULT_TASK_ID = DEFAULT_ID
DEFAULT_TABLE_ID = DEFAULT_ID
DEFAULT_WRITE_DISPOSITION_ID = DEFAULT_ID
DEFAULT_LOGIC_OPERATOR_ID = DEFAULT_ID
DEFAULT_OPERATOR_ID = DEFAULT_ID
DEFAULT_JOIN_ID = DEFAULT_ID


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
    name = models.CharField(
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


class JobTask(models.Model):
    name = models.CharField(
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
    )
    table_type = models.ForeignKey(
        TableType,
        on_delete=models.SET_DEFAULT,
        blank=False,
        null=False,
        default=DEFAULT_TABLE_ID,
        verbose_name="Target Table Type",
    )
    write_disposition = models.ForeignKey(
        WriteDisposition,
        on_delete=models.SET_DEFAULT,
        blank=False,
        null=False,
        default=DEFAULT_WRITE_DISPOSITION_ID,
        verbose_name="Write Disposition",
    )
    destination_table = models.CharField(
        verbose_name="Destination Table",
        max_length=255,
        blank=False,
        null=False,
    )
    destination_dataset = models.CharField(
        verbose_name="Destination Dataset",
        max_length=255,
        blank=True,
        null=True,
    )
    driving_table = models.CharField(
        verbose_name="Driving Table",
        max_length=255,
        blank=True,
        null=True,
    )
    staging_dataset = models.CharField(
        verbose_name="Staging Dataset",
        max_length=255,
        blank=True,
        null=True,
    )
    properties = models.JSONField(blank=True, null=True)
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


class History(models.Model):
    class Meta:
        verbose_name = "Historie"

    task = models.OneToOneField(
        JobTask, on_delete=models.CASCADE, blank=False, null=False
    )

    def __str__(self):
        return f"{self.task.name} history"


class Field(models.Model):
    name = models.CharField(
        verbose_name="Name", max_length=255, blank=False, null=False, help_text=""
    )
    source_column = models.CharField(
        verbose_name="Source Column",
        max_length=255,
        blank=True,
        null=True,
        help_text="",
    )
    source_name = models.CharField(
        verbose_name="Source Table",
        max_length=255,
        blank=True,
        null=True,
        help_text="",
    )
    transformation = models.CharField(
        verbose_name="Column Transformation",
        max_length=255,
        blank=True,
        null=True,
        help_text="",
    )
    is_source_to_target = models.BooleanField(default=True)
    is_primary_key = models.BooleanField(verbose_name="Primary Key Field")
    is_history_key = models.BooleanField(verbose_name="History Key Field")
    task = models.ForeignKey(JobTask, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class Dependency(models.Model):
    class Meta:
        verbose_name = "Dependencie"

    predecessor = models.ForeignKey(
        JobTask, on_delete=models.CASCADE, null=False, related_name="predecessor"
    )
    dependant = models.ForeignKey(
        JobTask, on_delete=models.CASCADE, null=False, related_name="dependant"
    )


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
        History, on_delete=models.CASCADE, blank=False, null=False
    )
    position = models.IntegerField(null=False)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=False)
    is_desc = models.BooleanField()

    def __str__(self):
        return f"Order By - {self.position}"


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
    )
    upper_bound = models.IntegerField(
        null=True, help_text="Input seconds to add to lower_bound"
    )


class Join(models.Model):
    left = models.CharField(
        verbose_name="Left Table",
        max_length=255,
        blank=True,
        null=True,
        help_text="Leave blank to default to driving table.",
    )
    right = models.CharField(
        verbose_name="Right Table",
        max_length=255,
        blank=False,
        null=False,
    )
    type = models.ForeignKey(
        JoinType, on_delete=models.SET_DEFAULT, null=False, default=DEFAULT_JOIN_ID
    )
    task = models.ForeignKey(JobTask, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.task.name} join to {self.right}"


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
    join = models.ForeignKey(Join, on_delete=models.SET_NULL, null=True, blank=True)
    where = models.ForeignKey(JobTask, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.join.task.name if self.join else (self.where.task.name if self.where else '')}{'Join Condition' if self.join else ('Where Condition' if self.where else '')}"


class ConditionField(models.Model):
    left = models.CharField(
        verbose_name="Left Parameter", blank=False, null=False, max_length=255
    )
    right = models.CharField(
        verbose_name="Right Parameter", blank=False, null=False, max_length=255
    )
    condition = models.OneToOneField(
        Condition, on_delete=models.CASCADE, null=False, blank=False
    )
