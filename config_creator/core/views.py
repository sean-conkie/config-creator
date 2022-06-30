import git
import hashlib
import json
import os
import re

from .forms import FieldForm, JobTaskForm, UploadFileForm
from .models import *
from accounts.models import GitRepository
from django.contrib import messages
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http import HttpResponseRedirect
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
class JobCreateView(CreateView):
    model = Job
    fields = ["name", "type", "description", "properties"]

    def form_valid(self, form):
        form.instance.createdby = self.request.user
        form.instance.updatedby = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("job-tasks", kwargs={"pk": self.pk})


class JobUpdateView(UpdateView):
    model = Job
    fields = ["name", "type", "description", "properties"]

    def form_valid(self, form):
        form.instance.updatedby = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy("jobs")


def jobsview(request):

    context = {"jobs": Job.objects.filter(createdby=request.user)}
    return render(
        request,
        "core/jobs.html",
        context,
    )


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


class JobTaskDeleteView(DeleteView):
    model = JobTask

    def get_success_url(self):
        return reverse("job-tasks", kwargs={"pk": self.job_id})


def jobtaskview(request, job_id, pk):
    task = JobTask.objects.select_related().get(id=pk)
    job = Job.objects.get(id=job_id)
    fields = Field.objects.filter(task_id=pk, is_source_to_target=True)
    joins = Join.objects.select_related().filter(task_id=pk)
    where = Condition.objects.select_related().filter(where=pk)
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
            reverse("job-task"),
            kwargs={
                "job_id": task.job_id,
                "pk": task.id,
            },
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

# region methods
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


# endregion
