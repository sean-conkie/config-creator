import sys

from django.db import models
from django.conf import settings
from django.db.models import Q
from django.urls import reverse

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
    "ConditionField",
    "BatchJobProperties",
    "DEFAULT_TASK_ID",
    "DEFAULT_TABLE_ID",
    "DEFAULT_WRITE_DISPOSITION_ID",
    "DEFAULT_LOGIC_OPERATOR_ID",
    "DEFAULT_OPERATOR_ID",
    "DEFAULT_JOIN_ID",
    "DagJobProperties",
    "BatchCustomJobTaskProperties",
]

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
                return property_class.objects.filter(
                    job_id=self.id,
                )[0]
            else:
                return property_class(
                    job_id=self.id,
                )

        return None


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
                return property_class.objects.filter(
                    task_id=self.id,
                )[0]
            else:
                return property_class(
                    task_id=self.id,
                )

        return None


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
        help_text="Source for the column, include dataset and table names: <dataset name>.<table name>",
    )
    transformation = models.CharField(
        verbose_name="Column Transformation",
        max_length=255,
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
    task = models.ForeignKey(JobTask, on_delete=models.CASCADE, null=False)

    def __str__(self):
        outp = []
        if self.source_name:
            outp.append(self.source_name)
        if self.source_column:
            outp.append(self.source_column)
        else:
            outp.append(self.name)

        return ".".join(outp)


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
        help_text="""Input a function that returns a date value or use preset;
$YESTERDAY = today's date minus one day
    $TODAY = today's date
 $THISWEEK = start date of current week, start date = MONDAY
$THISMONTH = date of first day of current month
""",
    )
    upper_bound = models.IntegerField(
        null=True,
        help_text="Input seconds to add to lower_bound, 86400 represents one day",
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
        return f"{self.join.task.name if self.join else (self.where.name if self.where else '')}{'Join Condition' if self.join else ('Where Condition' if self.where else '')}"


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

    class Meta:
        abstract = True


class BatchJobProperties(BaseJobProperties):
    prefix = models.CharField(
        verbose_name="Script Name Prefix",
        max_length=255,
        unique=False,
        blank=False,
        null=False,
        help_text="Enter the prefix which will be used for all tasks in this job; i.e. spine_order",
    )


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


class BaseJobTaskProperties(models.Model):
    task = models.OneToOneField(
        to=JobTask,
        on_delete=models.CASCADE,
        unique=True,
    )

    class Meta:
        abstract = True


class BatchCustomJobTaskProperties(BaseJobTaskProperties):
    sql = models.CharField(
        verbose_name="Sql Script Name",
        max_length=255,
        unique=False,
        blank=False,
        null=False,
        help_text="Enter the name of the sql fiel to be used by this task",
    )


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
