from .models import GitRepository
from database_interface_api.models import Connection
from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class RegisterForm(forms.ModelForm):
    """
    The default

    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "forename", "surname"]

    def clean_email(self):
        """
        Verify email is available.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        """
        Verify both passwords match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "email",
            "forename",
            "surname",
            "password1",
            "password2",
        ]

    def clean(self):
        """
        Verify both passwords match.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "forename",
            "surname",
            "password",
            "is_active",
            "admin",
            "git_username",
        ]

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = [
            "id",
            "name",
            "connectiontype",
        ]

        widgets = {
            "credentials": forms.ClearableFileInput(),
            "schema": AdminFileWidget(),
        }


class GitForm(forms.ModelForm):
    class Meta:
        model = GitRepository
        fields = [
            "id",
            "name",
            "url",
        ]
