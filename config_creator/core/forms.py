from .models import *
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


class JobTaskForm(forms.ModelForm):
    class Meta:
        model = JobTask
        fields = [
            "name",
            "type",
            "description",
            "properties",
            "write_disposition",
            "destination_table",
            "destination_dataset",
            "driving_table",
            "staging_dataset",
            "table_type",
            "job",
        ]


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = [
            "name",
            "source_column",
            "source_name",
            "transformation",
            "is_primary_key",
        ]
