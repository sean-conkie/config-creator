# Generated by Django 4.0.5 on 2022-10-01 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0043_auto_20220927_2019"),
    ]

    operations = [
        migrations.AlterField(
            model_name="batchcustomjobtaskproperties",
            name="sql",
            field=models.CharField(
                help_text="Enter the name of the sql field to be used by this task",
                max_length=255,
                verbose_name="SQL Script Name",
            ),
        ),
        migrations.CreateModel(
            name="TaskTypeToWriteDisposition",
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
                    "task_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.tasktype"
                    ),
                ),
                (
                    "write_disposition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.writedisposition",
                    ),
                ),
            ],
        ),
    ]