import json
import mimetypes
import os
import re

from .forms import (
    ConditionForm,
    DeltaForm,
    DependencyForm,
    FieldForm,
    JobForm,
    JobTaskForm,
    JoinForm,
    UploadFileForm,
    str_to_form,
)
from .models import *
from accounts.models import GitRepository
from database_interface_api.dbhelper import get_table_deletion_columns
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from lib.file_helper import file_upload
from lib.helper import safe_dict

__all__ = [
    "index",
    "loadfrom",
    "repositoriesview",
    "pullrepository",
    "pullnewrepository",
    "fileselect",
    "schema_fileselect",
    "editjobview",
    "editjobproperty",
    "jobdeleteview",
    "jobsview",
    "jobdownload",
    "jobtasksview",
    "jobtaskview",
    "jobtaskdeleteview",
    "editjobtaskview",
    "editjobtaskproperty",
    "editfieldview",
    "fieldview",
    "fielddeleteview",
    "editjoinview",
    "joindeleteview",
    "editconditionview",
    "conditiondeleteview",
    "editdeltaview",
    "deltadeleteview",
    "adddependencyview",
    "dependencydeleteview",
    "crawler",
    "gitfileselect",
]

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
        Repo.clone_from(repo.url, target_path)
    else:
        repo = Repo(target_path)
        git = repo.git
        git.pull()

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


def gitfileselect(request, path):
    id = handle_uploaded_file(request, path)
    return redirect(
        reverse(
            "job-tasks",
            kwargs={"job_id": id},
        )
    )


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
            return redirect(
                reverse(
                    "job-tasks",
                    kwargs={"job_id": id},
                )
            )
    else:
        form = UploadFileForm()
    return render(request, "fileselect.html", {"form": form})


def schema_fileselect(request):
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
            return redirect(
                reverse(
                    "job-tasks",
                    kwargs={"job_id", id},
                )
            )
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

        job.name = request.POST.get("name")
        job.description = request.POST.get("description")
        job.properties = request.POST.get("properties")
        job.type = JobType.objects.get(id=request.POST.get("type"))
        job.createdby = request.user
        job.updatedby = request.user
        job.save()

        property_object = job.get_property_object()

        if property_object:
            return redirect(
                reverse(
                    "job-property-add",
                    kwargs={
                        "job_id": job.id,
                    },
                ),
            )

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


def editjobproperty(request, job_id, pk=None):
    job = Job.objects.select_related().get(id=job_id)
    form = str_to_form(f"{job.get_property_object().__class__.__name__}Form")

    if request.method == "POST":
        return_form = form(request.POST)
        return_form.instance.job_id = job_id
        if pk:
            return_form.instance.id = pk
        if return_form.is_valid():
            return_form.save()
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
            edit_form = form(instance=job.get_property_object())
        else:
            edit_form = form()

        return render(
            request,
            "core/job_property_form.html",
            {
                "form": edit_form,
                "job_id": job.id,
                "pk": pk,
            },
        )


def jobdeleteview(request, pk):
    if request.method == "POST":
        Job.objects.get(id=pk).delete()
        messages.success(request, "Job deleted successfully.")

        return redirect(
            reverse(
                "jobs",
            )
        )
    else:
        return render(
            request,
            "core/confirm_delete.html",
            {
                "delete_url": reverse(
                    "job-delete",
                    kwargs={
                        "pk": pk,
                    },
                ),
                "return_url": reverse(
                    "job-task",
                    kwargs={
                        "pk": pk,
                    },
                ),
                "object": "job",
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

    file_name = f"cfg_{filecontent.get('name', 'config')}.json"
    mime_type, _ = mimetypes.guess_type(file_name)
    response = HttpResponse(c, content_type=mime_type)
    response["Content-Disposition"] = "attachment; filename=%s" % file_name
    return response


# endregion

# region task views
def jobtasksview(request, job_id):
    job = Job.objects.select_related().get(id=job_id)
    if job.get_property_object():
        job_property = job.get_property_object()
        properties = job_property.pprint()
        job_property_id = job_property.id
    else:
        properties = {}
        job_property_id = None
    context = {
        "job": job,
        "properties": [{k: properties.get(k)} for k in properties.keys()],
        "property_id": job_property_id,
        "tasks": JobTask.objects.select_related().filter(job=job),
    }
    return render(
        request,
        "core/job_tasks.html",
        context,
    )


def jobtaskdeleteview(request, job_id, pk):
    if request.method == "POST":
        JobTask.objects.get(id=pk).delete()
        messages.success(request, "Task deleted successfully.")

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
            "core/confirm_delete.html",
            {
                "delete_url": reverse(
                    "job-task-delete",
                    kwargs={
                        "job_id": job_id,
                        "pk": pk,
                    },
                ),
                "return_url": reverse(
                    "job-tasks",
                    kwargs={
                        "job_id": job_id,
                    },
                ),
                "object": "task",
            },
        )


def jobtaskview(request, job_id, pk, dependency_id=None, task_id=None):
    task = JobTask.objects.select_related().get(id=pk)
    job = Job.objects.get(id=job_id)
    fields = Field.objects.filter(task_id=pk, is_source_to_target=True).order_by(
        "position"
    )
    joins = get_joins(pk)
    where = get_where(pk)
    delta = Delta.objects.select_related().filter(task_id=pk)
    dependencies = Dependency.objects.select_related().filter(dependant=pk)

    if task.table_type != TableType.objects.get(code="TYPE1"):
        history = (
            History.objects.get(task_id=pk)
            if History.objects.filter(task_id=pk).exists()
            else History(task_id=pk).save()
        )
    else:
        history = None

    if history:
        partition = Partition.objects.select_related().filter(history_id=history.id)
        history_order = HistoryOrder.objects.select_related().filter(
            history_id=history.id
        )
        driving_column = DrivingColumn.objects.select_related().filter(
            history_id=history.id
        )

    source_tables = SourceTable.objects.filter(task_id=pk)
    if task.get_property_object():
        properties = safe_dict(task.get_property_object().pprint())
    else:
        properties = {}

    return render(
        request,
        "core/jobtask.html",
        {
            "task": task,
            "job": job,
            "fields": fields,
            "field_form": FieldForm(
                initial={
                    "data_type": 1,
                    "position": -1,
                }
            ),
            "joins": joins,
            "join_form": JoinForm(),
            "condition_form": ConditionForm(),
            "delta_form": DeltaForm(),
            "dependency_form": DependencyForm(),
            "where": where,
            "delta": delta,
            "dependencies": dependencies,
            "dependency_id": dependency_id,
            "task_id": task_id,
            "history": history,
            "driving_column": driving_column if history else [],
            "partition": partition if history else [],
            "history_order": history_order if history else [],
            "source_tables": source_tables,
            "properties": [{k: properties.get(k)} for k in properties.keys()],
        },
    )


def editjobtaskview(request, job_id, pk=None):
    if request.method == "POST":
        if request.POST["id"]:
            task = JobTask.objects.get(id=request.POST["id"])
        else:
            task = JobTask()

        m = re.search(
            r"^(?:(?P<project>[\w\-\d]+)\.)?(?:(?P<dataset_name>[\w\-\d]+)\.)(?P<table_name>[\w\-\d]+)(?: +(?P<alias>\w+))?$",
            request.POST.get("driving_table", ""),
            re.IGNORECASE,
        )

        task.name = request.POST["name"]
        task.description = request.POST["description"]
        task.destination_dataset = request.POST["destination_dataset"]
        task.destination_table = request.POST["destination_table"]
        task.driving_table = f"{m.group('dataset_name')}.{m.group('table_name')}"
        task.table_type = TableType.objects.get(id=request.POST["table_type"])
        task.write_disposition = WriteDisposition.objects.get(
            id=request.POST["write_disposition"]
        )
        task.staging_dataset = request.POST["staging_dataset"]
        task.type = TaskType.objects.get(id=request.POST["type"])
        if not task.id:
            task.createdby = request.user
        task.updatedby = request.user
        task.job_id = request.POST["job_id"]
        task.save()

        driving_table = get_source_table(
            task.id,
            m.group("dataset_name"),
            m.group("table_name"),
            "src",
            m.group("project"),
        )

        get_source_table(
            task.id,
            task.destination_dataset,
            task.destination_table,
            "trg",
            Job.objects.get(id=task.job_id).get_property_object().target_project,
        )

        get_table_deletion_columns(driving_table)

        if (
            task.table_type != TableType.objects.get(code="TYPE1")
            and not History.objects.filter(task_id=task.id).exists()
        ):
            History(task_id=task.id).save()

        property_object = task.get_property_object()

        if property_object:
            return redirect(
                reverse(
                    "job-task-property-add",
                    kwargs={
                        "job_id": job_id,
                        "task_id": task.id,
                    },
                ),
            )

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

        types = {
            type.name: [
                tttwd.write_disposition.todict()
                for tttwd in TaskTypeToWriteDisposition.objects.filter(task_type=type)
            ]
            for type in TaskType.objects.all()
        }

        job = Job.objects.get(id=job_id)

        return render(
            request,
            "core/jobtask_form.html",
            {
                "form": form,
                "types": types,
                "job": job,
                "task_id": pk,
            },
        )


def editjobtaskproperty(request, job_id, task_id, pk=None):
    task = JobTask.objects.select_related().get(id=task_id)
    form = str_to_form(f"{task.get_property_object().__class__.__name__}Form")

    if request.method == "POST":
        return_form = form(request.POST)
        return_form.instance.task_id = task_id
        if pk:
            return_form.instance.id = pk
        if return_form.is_valid():
            return_form.save()
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
            edit_form = form(instance=task.get_property_object())
        else:
            edit_form = form()

        return render(
            request,
            "core/jobtask_property_form.html",
            {
                "form": edit_form,
                "job_id": job_id,
                "task_id": task_id,
                "pk": pk,
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

        form = FieldForm(
            request.POST,
        )
        task = JobTask.objects.get(id=task_id)
        if request.POST.get("source_name", "") == "":
            form.instance.source_name = task.driving_table

        if request.POST.get("source_column", "") == "":
            form.instance.source_column = request.POST.get("name", "")

        if pk:
            message = f"{request.POST.get('name', 'Field')} updated successfully."
            form.instance.id = pk
            original_position = Field.objects.get(id=pk).position
        else:
            message = f"{request.POST.get('name', 'Field')} created successfully."
            original_position = -1

        form.instance.task_id = task_id

        if form.is_valid():
            form.save()
            changefieldposition(
                Field.objects.get(id=form.instance.id),
                original_position,
                form.instance.position,
            )
            messages.success(request, message)

        if request.POST.get("action") == "return":
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
            return redirect(
                reverse(
                    "job-task-field-add",
                    kwargs={
                        "job_id": job_id,
                        "task_id": task_id,
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
        Field.objects.get(id=pk).delete()
        messages.success(request, "Field deleted successfully.")

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
            "core/confirm_delete.html",
            {
                "delete_url": reverse(
                    "job-task-field-delete",
                    kwargs={
                        "job_id": job_id,
                        "task_id": task_id,
                        "pk": pk,
                    },
                ),
                "return_url": reverse(
                    "job-task",
                    kwargs={
                        "job_id": job_id,
                        "pk": task_id,
                    },
                ),
                "object": "field",
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

        if pk:
            messages.success(request, f"Join updated successfully.")
            return redirect(
                reverse(
                    "job-task",
                    kwargs={"job_id": job_id, "pk": task_id},
                ),
            )
        else:
            messages.success(request, f"Join created successfully.")
            return redirect(
                reverse(
                    "job-task-join-condition-add",
                    kwargs={"job_id": job_id, "task_id": task_id, "join_id": join.id},
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


def joindeleteview(request, job_id, task_id, pk):
    if request.method == "POST":
        Join.objects.get(id=pk).delete()
        messages.success(request, "Join deleted successfully.")

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
            "core/confirm_delete.html",
            {
                "delete_url": reverse(
                    "job-task-join-delete",
                    kwargs={
                        "job_id": job_id,
                        "task_id": task_id,
                        "pk": pk,
                    },
                ),
                "return_url": reverse(
                    "job-task",
                    kwargs={
                        "job_id": job_id,
                        "pk": task_id,
                    },
                ),
                "object": "join",
            },
        )


# endregion

# region condition views


def editconditionview(request, job_id, task_id, join_id=None, pk=None):

    if request.method == "POST":

        form = ConditionForm(request.POST)
        message = f"Condition created successfully."
        if pk:
            form.instance.id = pk
            message = f"Condition updated successfully."

        form.instance.join_id = join_id
        form.instance.where_id = task_id if not join_id else None

        pattern = r"(?P<dataset>\b\w+\b)\.(?P<table>\b\w+\b)\.(?P<field>\b\w+\b)"
        left = re.search(pattern, request.POST.get("left_field"), re.IGNORECASE)
        right = re.search(pattern, request.POST.get("right_field"), re.IGNORECASE)

        if (
            left
            and not Field.objects.filter(
                source_column=left.group("field"),
                source_name=f"{left.group('dataset')}.{left.group('table')}",
            ).exists()
        ):
            left_field = Field()
            left_field.source_column = left.group("field")
            left_field.source_name = f"{left.group('dataset')}.{left.group('table')}"
            left_field.is_source_to_target = False
            left_field.task_id = task_id
            left_field.save()
        elif left:
            left_field = Field.objects.get(
                source_column=left.group("field"),
                source_name=f"{left.group('dataset')}.{left.group('table')}",
            )
        else:
            left_field = Field(
                transformation=request.POST.get("left_field"),
                is_source_to_target=False,
                task_id=task_id,
            )
            left_field.save()

        if (
            right
            and not Field.objects.filter(
                source_column=right.group("field"),
                source_name=f"{right.group('dataset')}.{right.group('table')}",
            ).exists()
        ):
            right_field = Field()
            right_field.source_column = right.group("field")
            right_field.source_name = f"{right.group('dataset')}.{right.group('table')}"
            right_field.is_source_to_target = False
            right_field.task_id = task_id
            right_field.save()
        elif right:
            right_field = Field.objects.get(
                source_column=right.group("field"),
                source_name=f"{right.group('dataset')}.{right.group('table')}",
            )
        else:
            right_field = Field(
                transformation=request.POST.get("right_field"),
                is_source_to_target=False,
                task_id=task_id,
            )
            right_field.save()

        if form.is_valid():
            form.save()
            condition = Condition.objects.get(id=form.instance.id)
            condition.right_id = right_field.id
            condition.left_id = left_field.id
            condition.save()
            messages.success(request, message)

            return redirect(
                reverse(
                    "job-task",
                    kwargs={"job_id": job_id, "pk": task_id},
                ),
            )

        return render(
            request,
            "core/condition_form.html",
            {
                "form": form,
                "task": JobTask.objects.get(id=task_id),
                "job": Job.objects.get(id=job_id),
                "join_id": join_id,
                "condition_id": pk,
            },
        )

    else:
        if pk:
            condition = Condition.objects.select_related().get(id=pk)
            form = ConditionForm(instance=condition)
        else:
            condition = None
            form = ConditionForm()

        job = Job.objects.get(id=job_id)
        task = JobTask.objects.get(id=task_id)

        return render(
            request,
            "core/condition_form.html",
            {
                "form": form,
                "condition": condition,
                "task": task,
                "job": job,
                "join_id": join_id,
                "condition_id": pk,
            },
        )


def conditiondeleteview(request, job_id, task_id, pk):
    if request.method == "POST":
        Condition.objects.get(id=pk).delete()
        messages.success(request, "Condition deleted successfully.")

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
            "core/confirm_delete.html",
            {
                "delete_url": reverse(
                    "job-task-where-condition-delete",
                    kwargs={
                        "job_id": job_id,
                        "task_id": task_id,
                        "pk": pk,
                    },
                ),
                "return_url": reverse(
                    "job-task",
                    kwargs={
                        "job_id": job_id,
                        "pk": task_id,
                    },
                ),
                "object": "condition",
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
        Delta.objects.get(id=pk).delete()
        messages.success(request, "Delta conditions deleted successfully.")

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
            "core/confirm_delete.html",
            {
                "delete_url": reverse(
                    "job-task-delta-delete",
                    kwargs={
                        "job_id": job_id,
                        "task_id": task_id,
                        "pk": pk,
                    },
                ),
                "return_url": reverse(
                    "job-task",
                    kwargs={
                        "job_id": job_id,
                        "pk": task_id,
                    },
                ),
                "object": "delta condition",
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
        Dependency.objects.get(id=pk).delete()
        messages.success(request, "Dependency deleted successfully.")

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
            "core/confirm_delete.html",
            {
                "delete_url": reverse(
                    "job-task-dependency-delete",
                    kwargs={
                        "job_id": job_id,
                        "task_id": task_id,
                        "pk": pk,
                    },
                ),
                "return_url": reverse(
                    "job-task",
                    kwargs={
                        "job_id": job_id,
                        "pk": task_id,
                    },
                ),
                "object": "dependency",
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
        }
        for condition in Condition.objects.select_related().filter(where_id=task_id)
    ]


def handle_uploaded_file(request, path: str = None):
    """
    It takes a JSON file, parses it, and saves the data to the database

    Args:
      request: The request object
      path (str): str=None

    Returns:
      The job id is being returned.
    """

    if path:
        file = open(path, "r")
    else:
        file = file_upload(request).file
    filecontent = file.read()

    jscontent = json.loads(filecontent)

    job = Job(
        name=jscontent.get("name"),
        type=JobType.objects.get(code=jscontent.get("type").upper()),
        description=jscontent.get("description"),
        createdby=request.user,
        updatedby=request.user,
    )
    job.save()

    job_properties = job.get_property_object()
    for key in jscontent.get("properties", {}).keys():
        setattr(job_properties, key, jscontent.get("properties", {})[key])

    job_properties.save()

    tasks = jscontent.get("tasks")
    dependencies = []
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
            description=task.get("description"),
            createdby=request.user,
            updatedby=request.user,
        )

        t.save()

        # add dependencies to a list to add later, once
        # all tasks have been created
        for dependency in task.get("dependencies"):
            dependencies.append(
                {
                    "dependant": t.id,
                    "predecessor": dependency,
                }
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
                "source_to_target",
                "where",
                "joins",
                "history",
                "delta",
            ]
        }

        task_properties = t.get_property_object()
        if task_properties:
            for key in properties.keys():
                setattr(task_properties, key, properties[key])

            task_properties.save()

        for key in params.get("source_tables"):
            st = SourceTable(
                source_project=params.get("source_tables")[key].get("source_project"),
                dataset_name=params.get("source_tables")[key].get("dataset_name"),
                table_name=params.get("source_tables")[key].get("table_name"),
                alias=params.get("source_tables")[key].get("alias"),
                task=t,
            )
            st.save()

        for i, field in enumerate(params.get("source_to_target", [])):
            f = Field(
                name=field.get("name", field.get("source_column")),
                data_type=BigQueryDataType.objects.get(name=field.get("data_type"))
                if field.get("data_type")
                else BigQueryDataType.objects.get(id=DEFAULT_DATA_TYPE_ID),
                source_column=field.get("source_column"),
                source_table=get_source_table(
                    dataset_name=field.get("source_table").get("dataset_name"),
                    table_name=field.get("source_table").get("table_name"),
                    alias=field.get("source_table").get("alias"),
                    task_id=t.id,
                )
                if field.get("source_table")
                else None,
                transformation=field.get("transformation"),
                is_source_to_target=True,
                is_primary_key=field.get("is_primary_key", False),
                is_history_key=field.get("is_history_key", False),
                is_nullable=field.get("is_nullable", True),
                source_data_type=field.get("source_data_type"),
                default=field.get("default"),
                position=i + 1,
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

            fields = where.get("fields")

            condition_fields = save_condition_fields(fields, t.id)

            w.left = condition_fields[0]
            w.right = condition_fields[1]

            w.save()

        for join in params.get("joins", []):
            right = get_source_table(
                dataset_name=join.get("right", {}).get("dataset_name"),
                table_name=join.get("right", {}).get("table_name"),
                alias=join.get("right", {}).get("alias"),
                task_id=t.id,
            )

            left = get_source_table(
                dataset_name=join.get("left", {}).get("dataset_name"),
                table_name=join.get("left", {}).get("table_name"),
                alias=join.get("left", {}).get("alias"),
                task_id=t.id,
            )

            j = Join(
                left_table=left,
                right_table=right,
                type=JoinType.objects.get(code=join.get("type", "left").upper()),
                task=t,
            )

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

                fields = condition.get("fields")

                condition_fields = save_condition_fields(fields, t.id)

                c.left = condition_fields[0]
                c.right = condition_fields[1]

                c.save()

        history = params.get("history")

        if history:
            history_obj = History(
                task=t,
            )
            history_obj.save()

            for i, partition in enumerate(history.get("partition", [])):
                partition_field = get_field_from_dict(partition, t.id)
                partition_field.partition = i
                partition_field.save()

                partition_obj = Partition(
                    history=history_obj,
                    position=i,
                    field=partition_field,
                )
                partition_obj.save()

            for i, driving_column in enumerate(history.get("driving_column", [])):
                driving_column_field = get_field_from_dict(driving_column, t.id)
                driving_column_field.partition = i
                driving_column_field.save()

                driving_column_obj = DrivingColumn(
                    history=history_obj,
                    position=i,
                    field=driving_column_field,
                )
                driving_column_obj.save()

            for i, order in enumerate(history.get("order", [])):
                order_field = get_field_from_dict(order.get("field"), t.id)
                order_field.partition = i
                order_field.save()

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
                field=get_field_from_dict(delta.get("field", {}), t.id),
                lower_bound=delta.get("lower_bound"),
                upper_bound=delta.get("upper_bound"),
            )
            delta_obj.save()

    for dependency in dependencies:
        predecessor = JobTask.objects.get(
            job_id=job.id,
            name=dependency.get("predecessor"),
        )
        dep = Dependency(
            predecessor_id=predecessor.id,
            dependant_id=dependency.get("dependant"),
        )
        dep.save()

    return job.id


def get_field_from_dict(field_structure: dict, task_id: int) -> Field:
    """
    > This function takes a dictionary of field attributes and returns a Field object

    Args:
      field_structure (dict): a dictionary containing the field's information
      task_id (int): The id of the task that the field belongs to.

    Returns:
      A field object
    """

    if Field.objects.filter(
        name=field_structure.get("name", field_structure.get("source_column")),
        data_type=BigQueryDataType.objects.get(name=field_structure.get("data_type"))
        if field_structure.get("data_type")
        else BigQueryDataType.objects.get(id=DEFAULT_DATA_TYPE_ID),
        source_column=field_structure.get("source_column"),
        source_table=get_source_table(
            dataset_name=field_structure.get("source_table").get("dataset_name"),
            table_name=field_structure.get("source_table").get("table_name"),
            alias=field_structure.get("source_table").get("alias"),
            task_id=task_id,
        )
        if field_structure.get("source_table")
        else None,
        transformation=field_structure.get("transformation"),
        is_source_to_target=field_structure.get("is_source_to_target", True),
        is_primary_key=field_structure.get("is_primary_key", False),
        is_history_key=field_structure.get("is_history_key", False),
        is_nullable=field_structure.get("is_nullable", True),
        task_id=task_id,
        source_data_type=field_structure.get("source_data_type"),
        default=field_structure.get("default"),
    ).exists():
        f = Field.objects.get(
            name=field_structure.get("name", field_structure.get("source_column")),
            data_type=BigQueryDataType.objects.get(
                name=field_structure.get("data_type")
            )
            if field_structure.get("data_type")
            else BigQueryDataType.objects.get(id=DEFAULT_DATA_TYPE_ID),
            source_column=field_structure.get("source_column"),
            source_table=get_source_table(
                dataset_name=field_structure.get("source_table").get("dataset_name"),
                table_name=field_structure.get("source_table").get("table_name"),
                alias=field_structure.get("source_table").get("alias"),
                task_id=task_id,
            )
            if field_structure.get("source_table")
            else None,
            transformation=field_structure.get("transformation"),
            is_source_to_target=field_structure.get("is_source_to_target", True),
            is_primary_key=field_structure.get("is_primary_key", False),
            is_history_key=field_structure.get("is_history_key", False),
            is_nullable=field_structure.get("is_nullable", True),
            task_id=task_id,
            source_data_type=field_structure.get("source_data_type"),
            default=field_structure.get("default"),
        )
    else:

        f = Field(
            name=field_structure.get("name", field_structure.get("source_column")),
            data_type=BigQueryDataType.objects.get(
                name=field_structure.get("data_type")
            )
            if field_structure.get("data_type")
            else BigQueryDataType.objects.get(id=DEFAULT_DATA_TYPE_ID),
            source_column=field_structure.get("source_column"),
            source_table=get_source_table(
                dataset_name=field_structure.get("source_table").get("dataset_name"),
                table_name=field_structure.get("source_table").get("table_name"),
                alias=field_structure.get("source_table").get("alias"),
                task_id=task_id,
            )
            if field_structure.get("source_table")
            else None,
            transformation=field_structure.get("transformation"),
            is_source_to_target=field_structure.get("is_source_to_target", True),
            is_primary_key=field_structure.get("is_primary_key", False),
            is_history_key=field_structure.get("is_history_key", False),
            is_nullable=field_structure.get("is_nullable", True),
            task_id=task_id,
            source_data_type=field_structure.get("source_data_type"),
            default=field_structure.get("default"),
        )
        f.save()

    return f


def save_condition_fields(fields: list[str], task_id: int) -> list[Field]:
    """
    It takes a list of strings, and returns a list of Field objects

    Args:
      fields (list[str]): list[str]
      task_id (int): The id of the task that the join belongs to.
      join_id (int): The id of the join that this condition is for.

    Returns:
      A list of fields
    """
    outp = []
    for field in fields:
        if field:
            m = re.search(
                r"^(?P<alias>\b\w+\b)\.(?P<field>\b\w+\b)$",
                field,
                re.IGNORECASE,
            )
            if m:
                f = get_field_from_dict(
                    {
                        "name": m.group("field"),
                        "data_type": BigQueryDataType.objects.get(
                            id=DEFAULT_DATA_TYPE_ID
                        ),
                        "source_column": m.group("field"),
                        "source_table": SourceTable.objects.get(
                            alias=m.group("alias"),
                            task_id=task_id,
                        ).todict(),
                        "is_source_to_target": False,
                        "task_id": task_id,
                    },
                    task_id,
                )
            else:
                f = Field(
                    transformation=field,
                    is_source_to_target=False,
                    task_id=task_id,
                )

                f.save()

            outp.append(f)

        else:

            outp.append(field)

    return outp


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
    job_properties = safe_dict(job.get_property_object().__dict__)

    tasks = JobTask.objects.select_related().filter(job=job)

    task_list = []
    for task in tasks:
        task_properties = (
            safe_dict(task.get_property_object().__dict__)
            if task.get_property_object()
            else {}
        )
        t = {
            "task_id": task.name,
            "operator": task.type.code,
            "description": task.description,
            "parameters": {
                k: task_properties.get(k)
                for k in task_properties.keys()
                if k not in ["_state", "id", "task_id"]
            },
            "dependencies": [
                dependency.predecessor.name
                for dependency in Dependency.objects.select_related().filter(
                    dependant_id=task.id
                )
            ],
            "author": f"{task.updatedby.forename} {task.updatedby.surname}",
        }

        params = t["parameters"]

        params["source_tables"] = {
            st.alias: st.todict() for st in SourceTable.objects.filter(task_id=task.id)
        }

        params["source_to_target"] = [
            f.todict()
            for f in Field.objects.select_related()
            .filter(
                task_id=task.id,
                is_source_to_target=True,
            )
            .order_by("position")
        ]

        params["where"] = []
        for c in Condition.objects.select_related().filter(where_id=task.id):
            where = {
                "logic_operator": c.logic_operator.code,
                "operator": c.operator.symbol,
                "fields": [],
            }

            left = None
            if c.left.transformation:
                left = c.left.transformation
            elif c.left.source_table:
                left = f"{c.left.source_table.alias}.{c.left.source_column}"

            right = None
            if c.right.transformation:
                right = c.right.transformation
            elif c.right.source_table:
                right = f"{c.right.source_table.alias}.{c.left.source_column}"

            where["fields"] = [
                left,
                right,
            ]
            params["where"].append(where)

        params["joins"] = [
            {
                "left": j.left_table.todict(),
                "right": j.right_table.todict(),
                "type": j.type.code,
                "on": [
                    {
                        "logic_operator": c.logic_operator.code,
                        "operator": c.operator.symbol,
                        "fields": [
                            c.left.transformation
                            if c.left.transformation
                            else f"{c.left.source_table.alias}.{c.left.source_column}",
                            c.right.transformation
                            if c.right.transformation
                            else f"{c.right.source_table.alias}.{c.right.source_column}",
                        ],
                    }
                    for c in Condition.objects.select_related().filter(join_id=j.id)
                ],
            }
            for j in Join.objects.select_related().filter(task_id=task.id)
        ]
        history = (
            History.objects.get(task_id=task.id)
            if History.objects.filter(task_id=task.id).exists()
            else None
        )
        if history:
            params["history"] = {
                "partition": [
                    f.field.todict()
                    for f in Partition.objects.select_related().filter(
                        history_id=history.id
                    )
                ],
                "driving_column": [
                    f.field.todict()
                    for f in DrivingColumn.objects.filter(history_id=history.id)
                ],
                "order": [
                    {
                        "field": f.field.todict(),
                        "is_desc": f.is_desc,
                    }
                    for f in HistoryOrder.objects.filter(
                        history_id=history.id
                    ).order_by("position")
                ],
            }

        if Delta.objects.filter(task_id=task.id).exists():
            params["delta"] = Delta.objects.get(task_id=task.id).todict()

        params["destination_table"] = task.destination_table
        params["destination_dataset"] = task.destination_dataset
        params["write_disposition"] = task.write_disposition.code
        params["driving_table"] = task.driving_table
        params["staging_dataset"] = task.staging_dataset
        params["target_type"] = task.table_type.code
        params["block_data_check"] = True
        params["build_artifacts"] = True

        task_list.append(t)

    filecontent = {
        "name": job.name,
        "description": job.description,
        "type": job.type.code,
        "properties": {
            k: job_properties.get(k)
            for k in job_properties.keys()
            if k not in ["_state", "id", "job_id"]
        },
        "tasks": task_list,
        "author": f"{job.updatedby.forename} {job.updatedby.surname}",
    }

    return filecontent


# endregion
