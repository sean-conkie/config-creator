# Generated by Django 4.0.5 on 2022-07-12 19:09

from django.db import migrations, models
import django.db.models.deletion


def create_default_data_type(apps, schema_editor):
    bq_data_type = apps.get_model("core", "BigQueryDataType")
    bq_data_type(name="STRING").save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_batchjobproperties_dataset_publish_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BigQueryDataType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Data Type")),
            ],
        ),
        migrations.RunPython(create_default_data_type),
        migrations.AddField(
            model_name="field",
            name="position",
            field=models.IntegerField(
                default=-1,
                help_text="Enter the column's position within the target table",
                verbose_name="Ordinal Position",
            ),
        ),
        migrations.AddField(
            model_name="field",
            name="source_data_type",
            field=models.CharField(
                blank=True,
                help_text="Data type for the column at source",
                max_length=255,
                null=True,
                verbose_name="Source Data Type",
            ),
        ),
        migrations.CreateModel(
            name="BatchCustomJobTaskProperties",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sql",
                    models.CharField(
                        help_text="Enter the name of the sql fiel to be used by this task",
                        max_length=255,
                        verbose_name="Sql Script Name",
                    ),
                ),
                (
                    "task",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="core.jobtask"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="field",
            name="data_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="core.bigquerydatatype",
                verbose_name="Data Type",
            ),
        ),
    ]
