from .models import *
from django.contrib import admin


class HistoryInLine(admin.TabularInline):
    model = History
    fields = ("get_name",)
    readonly_fields = ("get_name",)
    show_change_link = True

    def get_name(self, obj):
        return obj.__str__()

    get_name.admin_order_field = "name"
    get_name.short_description = "Name"


class DrivingColumnInLine(admin.TabularInline):
    model = DrivingColumn
    extra = 1
    max_num = 1


class HistoryOrderInLine(admin.TabularInline):
    model = HistoryOrder
    extra = 1
    max_num = 1


class PartitionInLine(admin.TabularInline):
    model = Partition
    extra = 1
    max_num = 1


class FieldInLine(admin.TabularInline):
    model = Field
    extra = 1
    max_num = 1


class JoinInLine(admin.TabularInline):
    model = Join
    fields = ("get_name",)
    readonly_fields = ("get_name",)
    show_change_link = True
    extra = 0

    def get_name(self, obj):
        return obj.__str__()

    get_name.admin_order_field = "name"
    get_name.short_description = "Name"

    def has_add_permission(self, request, obj):
        return False


class DeltaInLine(admin.TabularInline):
    model = Delta
    show_change_link = True
    extra = 1
    max_num = 1


class JobTaskInLine(admin.TabularInline):
    model = JobTask
    fields = ["name", "type", "description", "lastupdate", "updatedby"]
    readonly_fields = ["name", "type", "description", "lastupdate", "updatedby"]
    show_change_link = True
    extra = 0

    def has_add_permission(self, request, obj):
        return False


class JoinConditionInLine(admin.TabularInline):
    model = Condition
    fields = ("get_name",)
    readonly_fields = ("get_name",)
    show_change_link = True
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def get_name(self, obj):
        return obj.__str__()

    get_name.admin_order_field = "name"
    get_name.short_description = "Name"


@admin.register(JobType)
@admin.register(JoinType)
@admin.register(TaskType)
@admin.register(TableType)
@admin.register(WriteDisposition)
@admin.register(Operator)
@admin.register(LogicOperator)
@admin.register(BigQueryDataType)
class TypeAdmin(admin.ModelAdmin):

    list_display = ["name", "description"]
    search_fields = ["name"]
    ordering = ["name"]
    filter_horizontal = ()


@admin.register(JobToTaskType)
class JobToTaskAdmin(admin.ModelAdmin):

    list_display = ["get_jobtype", "get_tasktype"]
    list_filter = ["jobtype", "tasktype"]

    search_fields = ["jobtype", "tasktype"]
    ordering = ["jobtype", "tasktype"]
    filter_horizontal = ()

    def get_jobtype(self, obj):
        return obj.jobtype.name

    get_jobtype.admin_order_field = "jobtype"
    get_jobtype.short_description = "Job Type"

    def get_tasktype(self, obj):
        return obj.tasktype.name

    get_tasktype.admin_order_field = "tasktype"
    get_tasktype.short_description = "Task Type"


@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):

    list_display = ["get_predecessor", "get_dependant"]
    list_filter = ["predecessor", "dependant"]

    search_fields = ["predecessor", "dependant"]
    ordering = ["predecessor", "dependant"]
    filter_horizontal = ()

    def get_predecessor(self, obj):
        return obj.predecessor.name

    get_predecessor.admin_order_field = "predecessor"
    get_predecessor.short_description = "Predecessor"

    def get_dependant(self, obj):
        return obj.dependant.name

    get_dependant.admin_order_field = "dependant"
    get_dependant.short_description = "Dependant"


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = ["name", "type", "description", "lastupdate", "updatedby"]
    list_filter = ["type"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "type",
                    "description",
                )
            },
        ),
        (
            "Job Properties",
            {"fields": ("properties",)},
        ),
        (
            "Job Details",
            {"fields": ("created", "createdby", "lastupdate", "updatedby")},
        ),
    )

    search_fields = ["name"]
    ordering = ["name"]
    readonly_fields = ["created", "createdby", "lastupdate", "updatedby"]
    inlines = [JobTaskInLine]
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        if not Job.objects.filter(name=obj.name).exists():
            obj.createdby = request.user
        obj.updatedby = request.user
        super().save_model(request, obj, form, change)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ["task", "get_job"]
    inlines = [
        DrivingColumnInLine,
        PartitionInLine,
        HistoryOrderInLine,
    ]

    def get_job(self, obj):
        return obj.task.job.name

    get_job.admin_order_field = "job"
    get_job.short_description = "Job"

    def save_model(self, request, obj, form, change):
        if obj.task.table_type == TableType.objects.get(code="TYPE1"):
            obj.task.table_type = TableType.objects.get(code="HISTORY")
            obj.task.save()
        super().save_model(request, obj, form, change)


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = [
        "operator",
        "logic_operator",
        "join",
        "where",
    ]
    list_filter = [
        "operator",
        "logic_operator",
    ]
    filter_horizontal = ()


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "source_column",
        "source_table",
        "get_task",
        "get_job",
        "is_source_to_target",
        "is_primary_key",
        "is_history_key",
    ]

    def get_job(self, obj):
        return obj.task.job.name

    get_job.admin_order_field = "job"
    get_job.short_description = "Job"

    def get_task(self, obj):
        return obj.task.name

    get_task.admin_order_field = "task"
    get_task.short_description = "Task"

    def save_model(self, request, obj, form, change):
        original_position = Field.objects.get(id=obj.id).position if obj.id else -1
        super().save_model(request, obj, form, change)

        changefieldposition(
            Field.objects.get(id=obj.id),
            original_position,
            obj.position,
        )


@admin.register(Join)
class JoinAdmin(admin.ModelAdmin):

    list_display = ["type", "right", "task", "get_job"]
    list_filter = ["task", "type"]
    search_fields = ["right"]
    ordering = ["right", "task"]
    inlines = [JoinConditionInLine]
    filter_horizontal = ()
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "task",
                    "type",
                ),
            },
        ),
        (
            "Tables",
            {
                "fields": (
                    "left",
                    "right",
                )
            },
        ),
    )

    def get_job(self, obj):
        return obj.task.job.name

    get_job.admin_order_field = "job"
    get_job.short_description = "Job"


@admin.register(JobTask)
class JobTaskAdmin(admin.ModelAdmin):

    list_display = ["name", "type", "job", "description", "lastupdate", "updatedby"]
    list_filter = ["job", "type"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "job",
                    "type",
                    "description",
                )
            },
        ),
        (
            "Target Table",
            {
                "fields": (
                    "destination_table",
                    "destination_dataset",
                    "write_disposition",
                    "table_type",
                )
            },
        ),
        (
            "Source Table",
            {"fields": ("driving_table",)},
        ),
        (
            "Task Properties",
            {
                "fields": (
                    "staging_dataset",
                    "properties",
                )
            },
        ),
        (
            "Task Details",
            {"fields": ("created", "createdby", "lastupdate", "updatedby")},
        ),
    )

    search_fields = ["name"]
    ordering = ["job", "name"]
    readonly_fields = ["created", "createdby", "lastupdate", "updatedby"]
    inlines = [FieldInLine, JoinInLine, DeltaInLine, HistoryInLine]
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        if not JobTask.objects.filter(name=obj.name, job=obj.job).exists():
            obj.createdby = request.user
        obj.updatedby = request.user
        super().save_model(request, obj, form, change)


@admin.register(SourceTable)
class SourceTableAdmin(admin.ModelAdmin):
    list_display = [
        "table_name",
        "dataset_name",
        "source_project",
        "get_task",
        "get_job",
        "alias",
        "base_alias",
    ]

    def get_job(self, obj):
        return obj.task.job.name

    get_job.admin_order_field = "job"
    get_job.short_description = "Job"

    def get_task(self, obj):
        return obj.task.name

    get_task.admin_order_field = "task"
    get_task.short_description = "Task"
