from .forms import UserAdminChangeForm
from .models import User
from database_interface_api.models import Connection
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.edit import FormView


class ProfileView(FormView):

    form_class = UserAdminChangeForm
    template_name = "account_profile.html"
    success_url = "/accounts/profile/"

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


class EditConnectionView(FormView):
    def form_valid(self, form):
        form.instance.connection = self.request.connection
        form.save()
        return super().form_valid(form)


@login_required
def connectionview(request):
    context = {"connections": Connection.objects.filter(user=request.user)}
    return render(request, "account_connections.html", context)
