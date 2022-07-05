import git
import hashlib
import json
import mimetypes
import os
import re
import tempfile

from .forms import (
    ConditionForm,
    DeltaForm,
    DependencyForm,
    FieldForm,
    JobForm,
    JobTaskForm,
    JoinForm,
    UploadFileForm,
)
from .models import *
from accounts.models import GitRepository
from database_interface_api.models import Connection, ConnectionType
from django.contrib import messages
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# region core views
def index(request):
    """
    "When the user visits the root URL, render the index.html template."

    The render function takes in a request object and a string representing the template to render. It
    then returns a response object that contains the rendered template

    Args:
      request: This is the request object that Django will pass to the view.

    Returns:
      The index.html file is being returned.
    """
    return render(request, "index.html")


def loadfrom(request):
    """
    It renders the loadfrom.html template

    Args:
      request: This is the request object that is sent to the view. It contains all the information
    about the request.

    Returns:
      The render function is being returned.
    """
    return render(request, "loadfrom.html")


# endregion

# region repo views
def repositoriesview(request):
    """
    It gets all the repositories for the current user and passes them to the template

    Args:
      request: The request object.

    Returns:
      A list of all the repositories that the user has access to.
    """
    context = {
        "repositories": GitRepository.objects.filter(user=request.user),
        "next": reverse_lazy("repositories"),
    }
    return render(
        request,
        "repositories.html",
        context,
    )


def pullrepository(request, pk):
    """
    It clones the repository into a folder, then creates a tree of the files in the repository

    Args:
      request: The request object.
      pk: The primary key of the GitRepository object.

    Returns:
      A list of dictionaries.
    """

    repo = GitRepository.objects.get(id=pk)
    target_path = os.path.join(os.getcwd(), f"repos/{request.user.id}/{repo.name}/")

    if not os.path.exists(target_path):
        git.Repo.clone_from(repo.url, target_path)

    context = {
        "repo": repo,
        "files": createtree(crawler(target_path)),
    }
    return render(
        request,
        "fileselect_git.html",
        context,
    )


def pullnewrepository(request):
    """
    It takes a POST request, creates a new GitRepository object, saves it, and redirects to the pull
    page

    Args:
      request: The request object.

    Returns:
      A redirect to the repository-pull page.
    """
    if request.method == "POST":
        repo = GitRepository()

        repo.name = request.POST["name"]
        repo.url = request.POST["url"]
        repo.user = request.user
        repo.save()
        return redirect(reverse("repository-pull", kwargs={"pk": repo.id}))
    else:
        redirect_url = reverse_lazy("repository-add")
        return redirect(redirect_url)


# endregion

# region local file views
def fileselect(request):
    """
    If the request is a POST request, then the form is valid, and the file is uploaded, then redirect to
    the success URL.

    If the request is a GET request, then the form is not valid, and the form is rendered.

    Args:
      request: The current request object.

    Returns:
      The form is being returned.
    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            id = handle_uploaded_file(request)
            return HttpResponseRedirect("/")
    else:
        form = UploadFileForm()
    return render(request, "fileselect.html", {"form": form})


# endregion

# region job views
def editjobview(request, pk=None):
    if request.method == "POST":
        if request.POST["id"]:
            job = Job.objects.get(id=request.POST["id"])
        else:
            job = Job()

        job.name = request.POST["name"]
        job.description = request.POST["description"]
        job.properties = request.POST["properties"]
        job.type = JobType.objects.get(id=request.POST["type"])
        job.createdby = request.user
        job.updatedby = request.user
        job.save()
        return redirect(
            reverse(
                "job-tasks",
                kwargs={
                    "job_id": job.id,
                },
            ),
        )
    else:
        if pk:
            job = Job.objects.select_related().get(id=pk)
            form = JobForm(instance=job)
        else:
            form = JobForm()

        return render(
            request,
            "core/job_form.html",
            {
                "form": form,
                "job_id": pk,
            },
        )


def jobdeleteview(request, pk):
    if request.method == "POST":
        try:
            Job.objects.get(id=pk).delete()
            messages.success(request, "Job deleted successfully.")
        except:
            pass

        return redirect(
            reverse(
                "jobs",
            )
        )
    else:
        return render(
            request,
            "core/job_confirm_delete.html",
            {
                "pk": pk,
            },
        )


def jobsview(request):

    context = {"jobs": Job.objects.filter(createdby=request.user)}
    return render(
        request,
        "core/jobs.html",
        context,
    )


def jobdownload(request, pk):
    filecontent = get_filecontent(pk)
    c = json.dumps(filecontent, indent=2).encode("utf-8")

    # file = tempfile.NamedTemporaryFile(suffix=".json")
    # file.write(c)
    file_name = f"{filecontent.get('name', 'config')}.json"
    mime_type, _ = mimetypes.guess_type(file_name)
    response = HttpResponse(c, content_type=mime_type)
    response["Content-Disposition"] = "attachment; filename=%s" % file_name
    return response


# endregion

# region task views
def jobtasksview(request, job_id):
    job = Job.objects.select_related().get(id=job_id)
    context = {
        "job": job,
        "tasks": JobTask.objects.select_related().filter(job=job),
    }
    return render(
        request,
        "core/job_tasks.html",
        context,
    )


def jobtaskdeleteview(request, job_id, pk):
    if request.method == "POST":
        try:
            JobTask.objects.get(id=pk).delete()
            messages.success(request, "Task deleted successfully.")
        except:
            pass

        return redirect(
            reverse(
                "job-tasks",
                kwargs={
                    "job_id": job_id,
                },
            )
        )
    else:
        return render(
            request,
            "core/jobtask_confirm_delete.html",
            {
                "job_id": job_id,
                "pk": pk,
            },
        )


def jobtaskview(request, job_id, pk, dependency_id=None, task_id=None):
    task = JobTask.objects.select_related().get(id=pk)
    job = Job.objects.get(id=job_id)
    fields = Field.objects.filter(task_id=pk, is_source_to_target=True)
    joins = get_joins(pk)
    where = get_where(pk)
    delta = Delta.objects.select_related().filter(task_id=pk)
    dependencies = Dependency.objects.select_related().filter(dependant=pk)
    history = History.objects.filter(task_id=pk)
    if history:
        partition = Partition.objects.filter(history_id=history.id)
        history_order = HistoryOrder.objects.filter(history_id=history.id)

    return render(
        request,
        "core/jobtask.html",
        {
            "task": task,
            "job": job,
            "fields": fields,
            "joins": joins,
            "where": where,
            "delta": delta,
            "dependencies": dependencies,
            "dependency_id": dependency_id,
            "task_id": task_id,
            "history": history,
            "partition": partition if history else [],
            "history_order": history_order if history else [],
        },
    )


def editjobtaskview(request, job_id, pk=None):
    if request.method == "POST":
        if request.POST["id"]:
            task = JobTask.objects.get(id=request.POST["id"])
        else:
            task = JobTask()

        task.name = request.POST["name"]
        task.description = request.POST["description"]
        task.destination_dataset = request.POST["destination_dataset"]
        task.destination_table = request.POST["destination_table"]
        task.driving_table = request.POST["driving_table"]
        task.table_type = TableType.objects.get(id=request.POST["table_type"])
        task.write_disposition = WriteDisposition.objects.get(
            id=request.POST["write_disposition"]
        )
        task.properties = request.POST["properties"]
        task.staging_dataset = request.POST["staging_dataset"]
        task.type = TaskType.objects.get(id=request.POST["type"])
        task.createdby = request.user
        task.updatedby = request.user
        task.job_id = request.POST["job_id"]
        task.save()
        return redirect(
            reverse(
                "job-task",
                kwargs={
                    "job_id": task.job_id,
                    "pk": task.id,
                },
            ),
        )
    else:
        if pk:
            task = JobTask.objects.select_related().get(id=pk)
            form = JobTaskForm(instance=task)
        else:
            form = JobTaskForm()

        types = TaskType.objects.all()
        table_types = TableType.objects.all()
        write_dispositions = WriteDisposition.objects.all()
        job = Job.objects.get(id=job_id)

        return render(
            request,
            "core/jobtask_form.html",
            {
                "form": form,
                "types": types,
                "table_types": table_types,
                "write_dispositions": write_dispositions,
                "job": job,
                "task_id": pk,
            },
        )


# endregion

# region field views
def editfieldview(
    request,
    job_id,
    task_id,
    pk=None,
):
    if request.method == "POST":
        if request.POST["id"]:
            field = Field.objects.get(id=request.POST["id"])
        else:
            field = Field()

        field.name = request.POST["name"]
        field.source_name = request.POST["source_name"]
        field.source_column = request.POST["source_column"]
        field.transformation = request.POST["transformation"]
        field.is_primary_key = (
            True if request.POST.get("is_primary_key", "off") == "on" else False
        )
        field.task_id = task_id
        task = JobTask.objects.get(id=task_id)
        if field.source_name == "":
            field.source_name = task.driving_table

        if field.source_column == "":
            field.source_column = field.name

        field.save()
        messages.success(request, f"{field.name} created successfully.")

        if request.POST.get("action") == "return":
            return redirect(
                reverse(
                    "job-task",
                    kwargs={
                        "job_id": job_id,
                        "pk": field.task_id,
                    },
                ),
            )
        else:
            return redirect(
                reverse(
                    "job-task-field-add",
                    kwargs={
                        "job_id": job_id,
                        "task_id": field.task_id,
                    },
                ),
            )
    else:
        if pk:
            field = Field.objects.select_related().get(id=pk)
            form = FieldForm(instance=field)
        else:
            form = FieldForm()

        job = Job.objects.get(id=job_id)
        task = JobTask.objects.get(id=task_id)

        return render(
            request,
            "core/field_form.html",
            {
                "form": form,
                "task": task,
                "job": job,
                "field_id": pk,
            },
        )


def fielddeleteview(request, job_id, task_id, pk):
    if request.method == "POST":
        try:
            Field.objects.get(id=pk).delete()
            messages.success(request, "Field deleted successfully.")
        except:
            pass

        return redirect(
            reverse(
                "job-task",
                kwargs={
                    "job_id": job_id,
                    "pk": task_id,
                },
            )
        )
    else:
        return render(
            request,
            "core/field_confirm_delete.html",
            {
                "job_id": job_id,
                "task_id": task_id,
                "pk": pk,
            },
        )


def fieldview(request, job_id, task_id, pk):

    field = Field.objects.select_related().get(id=pk)
    job = Job.objects.get(id=job_id)
    task = JobTask.objects.get(id=task_id)

    return render(
        request,
        "core/field.html",
        {
            "field": field,
            "task": task,
            "job": job,
            "field_id": pk,
        },
    )


# endregion

# region join views
def editjoinview(request, job_id, task_id, pk=None):
    if request.method == "POST":
        if request.POST["id"]:
            join = Join.objects.get(id=request.POST["id"])
        else:
            join = Join()

        join.left = request.POST["left"]
        if join.left == "":
            task = JobTask.objects.get(id=task_id)
            join.left = task.driving_table
        join.right = request.POST["right"]
        join.task_id = task_id
        join.save()
        messages.success(request, f"Join created successfully.")

        return redirect(
            reverse(
                "job-task-join",
                kwargs={"job_id": job_id, "task_id": task_id, "pk": join.id},
            ),
        )
    else:
        if pk:
            join = Join.objects.select_related().get(id=pk)
            form = JoinForm(instance=join)
        else:
            form = JoinForm()

        job = Job.objects.get(id=job_id)
        task = JobTask.objects.get(id=task_id)

        return render(
            request,
            "core/join_form.html",
            {
                "form": form,
                "task": task,
                "job": job,
                "join_id": pk,
            },
        )


def joinview(request, job_id, task_id, pk):

    join = Join.objects.select_related().get(id=pk)
    job = Job.objects.get(id=job_id)
    task = JobTask.objects.get(id=task_id)

    return render(
        request,
        "core/join.html",
        {
            "join": join,
            "task": task,
            "job": job,
            "field_id": pk,
        },
    )


def joindeleteview(request, job_id, task_id, pk):
    if request.method == "POST":
        try:
            Join.objects.get(id=pk).delete()
            messages.success(request, "Join deleted successfully.")
        except:
            pass

        return redirect(
            reverse(
                "job-task",
                kwargs={
                    "job_id": job_id,
                    "pk": task_id,
                },
            )
        )
    else:
        return render(
            request,
            "core/condition_confirm_delete.html",
            {
                "job_id": job_id,
                "task_id": task_id,
                "pk": pk,
            },
        )


# endregion

# region condition views


def editconditionview(request, job_id, task_id, join_id=None, pk=None):

    if request.method == "POST":
        if request.POST["id"]:
            condition = Condition.objects.get(id=request.POST["id"])
            field = ConditionField.objects.get(condition_id=request.POST["id"])
        else:
            condition = Condition()
            field = ConditionField()

        condition.operator = Operator.objects.get(
            id=request.POST.get("operator", DEFAULT_OPERATOR_ID)
        )
        condition.logic_operator = LogicOperator.objects.get(
            id=request.POST.get("logic_operator", DEFAULT_LOGIC_OPERATOR_ID)
        )
        condition.join_id = join_id
        condition.where_id = task_id if not join_id else None
        condition.save()

        field.left = request.POST["left"]
        field.right = request.POST["right"]
        field.condition = condition
        field.save()

        messages.success(request, f"Condition created successfully.")

        return redirect(
            reverse(
                "job-task",
                kwargs={"job_id": job_id, "pk": task_id},
            ),
        )
    else:
        if pk:
            condition = Condition.objects.get(id=pk)
            form = ConditionForm(instance=condition)
            fields = ConditionField.objects.filter(condition_id=condition.id)
        else:
            form = ConditionForm()
            fields = []

        job = Job.objects.get(id=job_id)
        task = JobTask.objects.get(id=task_id)

        return render(
            request,
            "core/condition_form.html",
            {
                "form": form,
                "task": task,
                "job": job,
                "join_id": join_id,
                "condition_id": pk,
                "fields": fields,
            },
        )


def conditiondeleteview(request, job_id, task_id, pk):
    if request.method == "POST":
        try:
            Condition.objects.get(id=pk).delete()
            messages.success(request, "Condition deleted successfully.")
        except:
            pass

        return redirect(
            reverse(
                "job-task",
                kwargs={
                    "job_id": job_id,
                    "pk": task_id,
                },
            )
        )
    else:
        return render(
            request,
            "core/condition_confirm_delete.html",
            {
                "job_id": job_id,
                "task_id": task_id,
                "pk": pk,
            },
        )


# endregion

# region delta


def editdeltaview(request, job_id, task_id, pk=None):

    if request.method == "POST":
        if request.POST.get("id"):
            delta = Delta.objects.get(id=request.POST.get("id"))
        else:
            delta = Delta()

        if request.POST.get("field"):
            delta.field_id = request.POST.get("field")
        elif request.POST.get("source_column"):
            delta.field = Field(
                name=request.POST.get("source_column"),
                source_column=request.POST.get("source_column"),
                source_name=request.POST.get(
                    "source_name", JobTask.objects.get(id=task_id).driving_table
                ),
            )
        elif request.POST.get("transformation"):
            delta.field = Field(
                name="f01",
                transformation=request.POST.get("transformation"),
            )
        else:
            messages.error(
                request,
                "A field is required, either select an existing field or add a new one.",
            )

            fields = Field.objects.filter(task_id=task_id)
            return render(
                request,
                "core/delta_form.html",
                {
                    "form": DeltaForm(request.POST),
                    "task": task,
                    "job": job,
                    "fields": fields,
                    "delta_id": pk,
                },
            )

        delta.lower_bound = request.POST.get("lower_bound")
        delta.upper_bound = request.POST.get("upper_bound")
        delta.task_id = task_id
        delta.save()
        messages.success(request, f"Delta condition created successfully.")

        return redirect(
            reverse(
                "job-task",
                kwargs={
                    "job_id": job_id,
                    "pk": task_id,
                },
            ),
        )
    else:
        if pk:
            delta = Delta.objects.select_related().get(id=pk)
            form = DeltaForm(instance=delta)
        else:
            form = DeltaForm()

        job = Job.objects.get(id=job_id)
        task = JobTask.objects.get(id=task_id)
        fields = Field.objects.filter(task_id=task_id)

        return render(
            request,
            "core/delta_form.html",
            {
                "form": form,
                "task": task,
                "job": job,
                "fields": fields,
                "delta_id": pk,
            },
        )


def deltadeleteview(request, job_id, task_id, pk):
    if request.method == "POST":
        try:
            Delta.objects.get(id=pk).delete()
            messages.success(request, "Delta conditions deleted successfully.")
        except:
            pass

        return redirect(
            reverse(
                "job-task",
                kwargs={
                    "job_id": job_id,
                    "pk": task_id,
                },
            )
        )
    else:
        return render(
            request,
            "core/delta_confirm_delete.html",
            {
                "job_id": job_id,
                "task_id": task_id,
                "pk": pk,
            },
        )


# endregion

# region dependency views


def adddependencyview(request, job_id, task_id):

    if request.method == "POST":
        Dependency(dependant_id=task_id, predecessor_id=request.POST.get("predecessor"))
        Dependency.save()
        messages.success(request, f"Dependency condition created successfully.")

        return redirect(
            reverse(
                "job-task",
                kwargs={
                    "job_id": job_id,
                    "pk": task_id,
                },
            ),
        )
    else:
        form = DependencyForm()
        job = Job.objects.get(id=job_id)
        task = JobTask.objects.get(id=task_id)
        tasks = JobTask.objects.filter(~Q(id=task_id), job_id=job_id)

        return render(
            request,
            "core/dependency_form.html",
            {
                "form": form,
                "task": task,
                "job": job,
                "tasks": tasks,
            },
        )


def dependencydeleteview(request, job_id, task_id, pk):
    if request.method == "POST":
        try:
            Dependency.objects.get(id=pk).delete()
            messages.success(request, "Dependency deleted successfully.")
        except:
            pass

        return redirect(
            reverse(
                "job-task",
                kwargs={
                    "job_id": job_id,
                    "pk": task_id,
                },
            )
        )
    else:
        return render(
            request,
            "core/dependency_confirm_delete.html",
            {
                "job_id": job_id,
                "task_id": task_id,
                "pk": pk,
            },
        )


# endregion

# region methods
def get_joins(task_id: str) -> list[dict]:
    """
    It returns a list of dictionaries, where each dictionary contains a join object and a list of
    dictionaries, where each dictionary contains a condition object and a list of condition field
    objects

    Args:
      task_id (str): The id of the task you want to get the joins for.

    Returns:
      A list of dictionaries.
    """
    join_objects = Join.objects.select_related().filter(task_id=task_id)
    if len(join_objects) == 0:
        return []
    return [
        {
            "join": j,
            "conditions": [
                {
                    "condition": condition,
                    "fields": ConditionField.objects.filter(condition_id=condition.id),
                }
                for condition in Condition.objects.filter(join_id=j.id)
            ],
        }
        for j in join_objects
    ]


def get_where(task_id: str) -> list[dict]:
    """
    It returns a list of dictionaries, where each dictionary contains a condition and the fields
    associated with that condition

    Args:
      task_id (str): The ID of the task you want to get the conditions for.

    Returns:
      A list of dictionaries.
    """
    return [
        {
            "condition": condition,
            "fields": ConditionField.objects.filter(condition_id=condition.id),
        }
        for condition in Condition.objects.filter(where_id=task_id)
    ]


def handle_uploaded_file(request):

    upload = TemporaryFileUploadHandler(request)
    upload.new_file(
        request.FILES["file"].name,
        request.FILES["file"].name,
        "application/octet-stream",
        -1,
    )
    hash = hashlib.sha256()

    chunk = True
    size = 0
    while chunk:
        chunk = request.FILES["file"].read(upload.chunk_size)
        upload.receive_data_chunk(chunk, size)
        hash.update(chunk)
        size += len(chunk)
    upload.file_complete(size)

    filecontent = upload.file.read()
    jscontent = json.loads(filecontent)

    job = Job(
        name=jscontent.get("name"),
        type=JobType.objects.get(code=jscontent.get("type").upper()),
        description=jscontent.get("description"),
        properties=jscontent.get("properties"),
        createdby=request.user,
        updatedby=request.user,
    )
    job.save()

    tasks = jscontent.get("tasks")
    for task in tasks:
        params = task.get("parameters", {})
        t = JobTask(
            name=task.get("task_id"),
            job=job,
            type=TaskType.objects.get(code=task.get("operator").upper()),
            table_type=TableType.objects.get(
                code=params.get("target_type", "TYPE1").upper()
            ),
            write_disposition=WriteDisposition.objects.get(
                code=params.get("write_disposition", "WRITETRUNCATE").upper()
            ),
            destination_table=params.get("destination_table"),
            destination_dataset=params.get("destination_dataset"),
            driving_table=params.get("driving_table"),
            staging_dataset=params.get("staging_dataset"),
            description=params.get("description"),
            createdby=request.user,
            updatedby=request.user,
        )
        properties = {
            k: params[k]
            for k in params.keys()
            if k
            not in [
                "operator",
                "target_type",
                "write_disposition",
                "destination_table",
                "destination_dataset",
                "driving_table",
                "staging_dataset",
                "description",
            ]
        }
        t.properties = properties
        t.save()

        for field in params.get("source_to_target", []):
            f = Field(
                name=field.get("name", field.get("source_column")),
                source_column=field.get("source_column"),
                source_name=field.get("source_name"),
                transformation=field.get("transformation"),
                is_source_to_target=True,
                is_primary_key=field.get("is_primary_key", False),
                is_history_key=field.get("is_history_key", False),
                task=t,
            )
            f.save()

        for where in params.get("where", []):
            w = Condition(
                operator=Operator.objects.get(symbol=where.get("operator", "=")),
                logic_operator=LogicOperator.objects.get(
                    code=where.get("condition", "AND").upper()
                ),
                where=t,
            )
            w.save()

            fields = where.get("fields")
            field = ConditionField(
                left=fields[0],
                right=fields[1],
                condition=w,
            )
            field.save()

        for join in params.get("joins", []):
            j = Join(
                right=join.get("right"),
                type=JoinType.objects.get(code=join.get("type", "left").upper()),
                task=t,
            )
            if join.get("left"):
                j.left = join.get("left")

            j.save()

            for condition in join.get("on", []):
                c = Condition(
                    operator=Operator.objects.get(
                        symbol=condition.get("operator", "=")
                    ),
                    logic_operator=LogicOperator.objects.get(
                        code=condition.get("condition", "AND").upper()
                    ),
                    join=j,
                )
                c.save()

                fields = condition.get("fields")
                field = ConditionField(
                    left=fields[0],
                    right=fields[1],
                    condition=c,
                )
                field.save()

        history = params.get("history")

        if history:
            history_obj = History(
                task=t,
            )
            history_obj.save()

            for i, partition in enumerate(history.get("partition", [])):
                partition_field = Field.objects.get(
                    name=partition.get("name"),
                    source_column=partition.get("source_column"),
                    source_name=partition.get("source_name"),
                    transformation=partition.get("transformation"),
                )
                partition_field.is_history_key = True
                partition_field.save()

                partition_obj = Partition(
                    history=history_obj,
                    position=i,
                    field=partition_field,
                )
                partition_obj.save()

            for i, driving_column in enumerate(history.get("driving_column", [])):
                driving_column_field = Field.objects.get(
                    name=driving_column.get("name"),
                    source_column=driving_column.get("source_column"),
                    source_name=driving_column.get("source_name"),
                    transformation=driving_column.get("transformation"),
                )

                driving_column_obj = DrivingColumn(
                    history=history_obj,
                    position=i,
                    field=driving_column_field,
                )
                driving_column_obj.save()

            for i, order in enumerate(history.get("order", [])):
                order_field = Field.objects.get(
                    name=order.get("name"),
                    source_column=order.get("source_column"),
                    source_name=order.get("source_name"),
                    transformation=order.get("transformation"),
                )

                order_obj = HistoryOrder(
                    history=history_obj,
                    position=i,
                    field=order_field,
                )
                order_obj.save()

        delta = params.get("delta")
        if delta:
            delta_obj = Delta(
                task=t,
                field=Field.objects.get(
                    name=delta.get("name"),
                    source_column=delta.get("source_column"),
                    source_name=delta.get("source_name"),
                    transformation=delta.get("transformation"),
                ),
                lower_bound=delta.get("lower_bound"),
                upper_bound=delta.get("upper_bound"),
            )
            delta_obj.save()

    return job.id


def createtree(treesource: list[dict], layers: int = 1) -> list[str]:
    """
    It takes a list of dictionaries, and returns a list of strings

    Args:
      treesource (list[dict]): This is the list of dictionaries that you want to create the tree from.
      layers (int): This is the number of layers deep the current tree is. It's used to calculate the
    padding of the tree. Defaults to 1

    Returns:
      A list of strings.
    """
    outp = []
    padding = f"{layers * 10}"
    for n in treesource:
        if n.get("type") == "file":
            outp.append(
                f'<div style="padding-left: {padding}px;"><button class="tree-file" data-path="{n.get("path")}"><i class="bi bi-file-earmark-text"></i> {n.get("name")}</button></div>'
            )
        else:
            outp.append(
                f'<details  style="padding-left: {padding}px;"><summary class="tree-dir"><i class="bi bi-folder"></i> {n.get("name")}</summary>'
            )
            outp.extend(createtree(n.get("files"), layers=layers + 1))
            outp.append("</details>")

    return outp


def crawler(path: str, ignore_hidden: bool = True) -> list[dict]:
    """
    It crawls a directory and returns a list of dictionaries, each dictionary representing a file or
    directory

    Args:
      path (str): The path to the directory you want to crawl.
      ignore_hidden (bool): If True, ignore hidden files and directories. Defaults to True

    Returns:
      A list of dictionaries.
    """

    files = []
    for obj in os.listdir(path):
        obj_path = os.path.normpath(os.path.join(path, obj))
        file = {
            "name": obj,
            "path": os.path.relpath(obj_path),
        }
        pattern = r"^\.\w+$"
        match = re.search(pattern, obj, re.IGNORECASE)
        if match and ignore_hidden:
            continue
        if os.path.isfile(obj_path):
            file["type"] = "file"
        else:
            file["type"] = "dir"
            file["files"] = crawler(obj_path)
        files.append(file)
    return files


def get_filecontent(pk: int) -> dict:
    """
    It takes a job id, and returns a dictionary containing the job's name, description, type,
    properties, and a list of tasks

    Args:
      pk (int): the primary key of the job

    Returns:
      A dictionary with the job name, description, type, properties, and tasks.
    """
    job = Job.objects.select_related().get(id=pk)
    if job.properties and job.properties != "":
        job_properties = json.loads(job.properties)

    tasks = JobTask.objects.select_related().filter(job=job)

    task_list = []
    for task in tasks:
        t = {
            "task_id": task.name,
            "operator": task.type.code,
            "parameters": json.loads(
                task.properties
                if task.properties != "" and not task.properties is None
                else "{}"
            ),
            "description": job.description,
            "dependencies": [],
        }

        params = t["parameters"]

        params["source_to_target"] = [
            {
                "name": f.name,
                "source_column": f.source_column,
                "source_name": f.source_name,
                "transformation": f.transformation,
                "pk": f.is_primary_key,
                "hk": f.is_history_key,
            }
            for f in Field.objects.select_related().filter(
                task_id=task.id, is_source_to_target=True
            )
        ]

        params["where"] = [
            {
                "logic_operator": c.logic_operator.code,
                "operator": c.operator.symbol,
                "fields": [
                    [cf.left, cf.right]
                    for cf in ConditionField.objects.filter(condition_id=c.id)
                ][0],
            }
            for c in Condition.objects.select_related().filter(where_id=task.id)
        ]

        params["joins"] = [
            {
                "left": j.left,
                "right": j.right,
                "type": j.type.code,
                "on": [
                    {
                        "logic_operator": c.logic_operator.code,
                        "operator": c.operator.symbol,
                        "fields": [
                            [cf.left, cf.right]
                            for cf in ConditionField.objects.filter(condition_id=c.id)
                        ][0],
                    }
                    for c in Condition.objects.select_related().filter(join_id=j.id)
                ],
            }
            for j in Join.objects.select_related().filter(task_id=task.id)
        ]

        params["destination_table"] = task.destination_table
        params["destination_dataset"] = task.destination_dataset
        params["write_disposition"] = task.write_disposition.code
        params["driving_table"] = task.driving_table
        params["staging_dataset"] = task.staging_dataset
        params["target_type"] = task.table_type.code

        dependencies = [dependant.name for dependant in Dependency.objects.select_related().filter(dependant_id=task.id)]

        task_list.append(t)

    filecontent = {
        "name": job.name,
        "description": job.description,
        "type": job.type.code,
        "properties": job_properties,
        "tasks": task_list,
    }

    return filecontent


# endregion
