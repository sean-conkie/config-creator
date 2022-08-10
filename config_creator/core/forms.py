import sys

from .models import (
    BigQueryDataType,
    Job,
    JobTask,
    Field,
    Join,
    Condition,
    Delta,
    Dependency,
    BatchJobProperties,
    DagJobProperties,
    BatchCustomJobTaskProperties,
)
from django import forms
from django.core.exceptions import ValidationError

__all__ = [
    "UploadFileForm",
    "JobTaskForm",
    "FieldForm",
    "JoinForm",
    "ConditionForm",
    "DeltaForm",
    "DependencyForm",
    "JobForm",
    "BatchJobPropertiesForm",
    "DagJobPropertiesForm",
]


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

    data_type = forms.ModelChoiceField(
        queryset=BigQueryDataType.objects.order_by("name")
    )

    class Meta:
        model = Field
        fields = [
            "name",
            "source_column",
            "source_name",
            "transformation",
            "is_primary_key",
            "is_nullable",
            "position",
            "data_type",
            "source_data_type",
        ]


class JoinForm(forms.ModelForm):
    class Meta:
        model = Join
        fields = [
            "type",
            "left_table",
            "right_table",
        ]


class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = [
            "operator",
            "logic_operator",
            "left",
            "right",
        ]


class DeltaForm(forms.ModelForm):
    class Meta:
        model = Delta
        fields = [
            "field",
            "lower_bound",
            "upper_bound",
        ]


class DependencyForm(forms.ModelForm):
    class Meta:
        model = Dependency
        fields = [
            "predecessor",
            "dependant",
        ]


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "name",
            "type",
            "description",
            "id",
        ]


class BatchJobPropertiesForm(forms.ModelForm):
    class Meta:
        model = BatchJobProperties
        fields = [
            "prefix",
            "dataset_source",
            "dataset_staging",
            "dataset_publish",
            "source_project",
            "target_project",
        ]


class DagJobPropertiesForm(forms.ModelForm):
    class Meta:
        model = DagJobProperties
        fields = [
            "dataset_source",
            "dataset_staging",
            "dataset_publish",
            "owner",
            "email",
            "tags",
            "imports",
        ]


class BatchCustomJobTaskPropertiesForm(forms.ModelForm):
    class Meta:
        model = BatchCustomJobTaskProperties
        fields = [
            "sql",
        ]


def str_to_form(formname):
    """
    It takes a string and returns a form

    Args:
      formname: The name of the form to be loaded.

    Returns:
      The form object.
    """
    try:
        return getattr(sys.modules[__name__], formname)
    except AttributeError:
        return None
