from .forms import ConnectionForm, GitForm, UserAdminChangeForm
from .models import GitRepository, User
from database_interface_api.models import Connection, ConnectionType
from django.core.files import File
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, FormView


class ProfileView(FormView):

    form_class = UserAdminChangeForm
    template_name = "account_profile.html"
    success_url = reverse_lazy("profile")

    def get_form(self):
        """
        If the user exists, return the form with the user's data, otherwise return the form without the
        user's data

        Returns:
          The form_class is being returned.
        """
        try:
            profile = User.objects.get(id=self.request.user.id)
            return self.form_class(instance=profile, **self.get_form_kwargs())
        except User.DoesNotExist:
            return self.form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        """
        The function form_valid() is a method of the class CreateView. It is called when the form is
        valid. It saves the form and returns a HttpResponseRedirect to the success_url

        Args:
          form: The form that was submitted.

        Returns:
          The super().form_valid(form) is being returned.
        """
        form.instance.user = self.request.user
        form.instance.is_active = self.request.user.is_active
        form.instance.admin = self.request.user.admin
        form.instance.staff = self.request.user.staff
        form.save()
        return super().form_valid(form)


def editconnectionview(request, pk=None):
    """
    If the request is a POST, then we either create a new connection or update an existing one.

    If the request is a GET, then we redirect to the appropriate page.

    Let's break this down a bit.

    First, we check if the request is a POST. If it is, then we check if the request contains an id. If
    it does, then we get the connection with that id. If it doesn't, then we create a new connection.

    Next, we set the connection's name, connectionstring, connectiontype, and user.

    Finally, we save the connection.

    If the request is a GET, then we redirect to the appropriate page.

    Let's add the following to the bottom of the file:

    Args:
      request: The request object.
      pk: The primary key of the connection to edit.

    Returns:
      The view is returning a redirect to the url specified in the redirect_url variable.
    """
    if request.method == "POST":
        form = ConnectionForm(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            if "schema" in request.FILES.keys():
                form.instance.schema.save(
                    request.FILES.get("schema").name, File(request.FILES.get("schema"))
                )
            if "credentials" in request.FILES.keys():
                form.instance.credentials.save(
                    request.FILES.get("credentials").name,
                    File(request.FILES.get("credentials")),
                )
            form.save()

        return redirect(reverse_lazy("connections"))
    else:
        redirect_url = (
            reverse_lazy("connection-update", kwargs={"pk": pk})
            if pk
            else reverse_lazy("connections-add")
        )
        return redirect(redirect_url)


def connectionview(request, pk=None):
    """
    It takes a request and a primary key (pk) as arguments, and if the pk is not None, it gets the
    connection object with the given pk, and creates a form with that connection object as the instance.
    If the pk is None, it creates a blank form. It then gets all the connection types, and renders the
    connection form template with the form and types as context

    Args:
      request: The request object.
      pk: The primary key of the connection to edit. If it's None, we're creating a new connection.

    Returns:
      A form to create a new connection.
    """

    if pk:
        connection = Connection.objects.select_related().get(id=pk)
        form = ConnectionForm(instance=connection)
    else:
        form = ConnectionForm()

    types = ConnectionType.objects.all()

    return render(
        request,
        "database_interface_api/connection_form.html",
        {"form": form, "types": types},
    )


class ConnectionDeleteView(DeleteView):
    model = Connection
    success_url = reverse_lazy("connections")


def connectionsview(request):
    """
    It gets all the connections for the current user and passes them to the template

    Args:
      request: The request object.

    Returns:
      The request, the template, and the context.
    """
    context = {"connections": Connection.objects.filter(user=request.user)}
    return render(
        request,
        "account_connections.html",
        context,
    )


def repositoriesview(request):
    """
    It gets all the repositories for the current user and passes them to the template

    Args:
      request: The request object.

    Returns:
      A list of all the repositories that the user has access to.
    """
    context = {"repositories": GitRepository.objects.filter(user=request.user)}
    return render(
        request,
        "account_repositories.html",
        context,
    )


class RepositoryDeleteView(DeleteView):
    model = GitRepository
    success_url = reverse_lazy("repositories")


def repositoryview(request, pk=None, next=None):
    """
    If the user is requesting a specific repository, then get that repository and pass it to the form,
    otherwise just pass an empty form.

    Args:
      request: The request object.
      pk: The primary key of the object to edit.

    Returns:
      A form object
    """

    if pk:
        repository = GitRepository.objects.select_related().get(id=pk)
        form = GitForm(instance=repository)
    else:
        form = GitForm()

    return render(
        request,
        "repository_form.html",
        {
            "form": form,
            "next": next,
        },
    )


def editrepositoryview(request, pk=None):
    """
    It takes a POST request, and if it has an ID, it updates the repository with that ID, otherwise it
    creates a new repository

    Args:
      request: The request object.
      pk: The primary key of the object to be edited.

    Returns:
      A redirect to the url specified in the redirect_url variable.
    """
    if request.method == "POST":
        if request.POST["id"]:
            repo = GitRepository.objects.get(id=request.POST["id"])
        else:
            repo = GitRepository()

        repo.name = request.POST["name"]
        repo.url = request.POST["url"]
        repo.user = request.user
        repo.save()
        return redirect(reverse_lazy("repositories"))
    else:
        redirect_url = (
            reverse_lazy("repository-update", kwargs={"pk": pk})
            if pk
            else reverse_lazy("repository-add")
        )
        return redirect(redirect_url)
