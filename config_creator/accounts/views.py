from .forms import UserAdminChangeForm, ConnectionForm
from .models import User
from database_interface_api.models import Connection, ConnectionType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, resolve
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView


class ProfileView(FormView):

    form_class = UserAdminChangeForm
    template_name = "account_profile.html"
    success_url = reverse_lazy("profile")

    def get_form(self):
        """
        Check if the user already saved contact details. If so, then show
        the form populated with those details, to let user change them.
        """
        try:
            profile = User.objects.get(id=self.request.user.id)
            return self.form_class(instance=profile, **self.get_form_kwargs())
        except User.DoesNotExist:
            return self.form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_active = self.request.user.is_active
        form.instance.admin = self.request.user.admin
        form.instance.staff = self.request.user.staff
        form.save()
        return super().form_valid(form)


def editconnectionview(request, pk=None):
    if request.method == "POST":
        if request.POST["id"]:
            connection = Connection.objects.get(id=request.POST["id"])
        else:
            connection = Connection()

        connection.name = request.POST["name"]
        connection.connectionstring = request.POST["connectionstring"]
        connection.connectiontype = ConnectionType.objects.get(
            id=request.POST["connectiontype"]
        )
        connection.user = request.user
        connection.save()
        return redirect(reverse_lazy("connections"))
    else:
        redirect_url = (
            reverse_lazy("connection-update", kwargs={"pk": pk})
            if pk
            else reverse_lazy("connections-add")
        )
        return redirect(redirect_url)


def connectionview(request, pk=None):

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


@login_required
def connectionsview(request):
    context = {"connections": Connection.objects.filter(user=request.user)}
    return render(
        request,
        "account_connections.html",
        context,
    )
