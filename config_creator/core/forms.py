from django import forms
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    if not value.name.endswith(".json"):
        raise ValidationError("Only JSON files can be loaded.", code="invalid")


class UploadFileForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"hidden": True}),
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={"class": "box__file"}),
        validators=[validate_file_extension],
    )
