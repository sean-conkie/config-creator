import git
import os
import re

from accounts.models import GitRepository
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse


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

    return render(request, "loadfrom.html")


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
        "select_file_git.html",
        context,
    )


def pullnewrepository(request):
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


def createtree(treesource: list[dict], layers: int = 1) -> list[str]:
    """
    It takes a list of files and folders and returns a list of HTML elements

    Args:
      treesource (lis): The source of the tree. This is a dictionary with the following keys:

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
