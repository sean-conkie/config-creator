# Generated by Django 4.0.5 on 2022-06-21 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_jobtask_description_alter_job_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobtask",
            name="staging_dataset",
            field=models.CharField(max_length=255, verbose_name="Staging Dataset"),
        ),
        migrations.CreateModel(
            name="Partition",
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
                ("position", models.IntegerField()),
                (
                    "field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.field"
                    ),
                ),
                (
                    "history",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.history"
                    ),
                ),
            ],
        ),
    ]
