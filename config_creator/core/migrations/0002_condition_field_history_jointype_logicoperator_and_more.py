# Generated by Django 4.0.5 on 2022-06-21 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Condition",
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
            ],
        ),
        migrations.CreateModel(
            name="Field",
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
                    "name",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
                (
                    "source_column",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
                (
                    "source_name",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
                (
                    "transformation",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
                ("is_source_to_target", models.BooleanField()),
                (
                    "is_primary_key",
                    models.BooleanField(verbose_name="Primary Key Field"),
                ),
                (
                    "is_history_key",
                    models.BooleanField(verbose_name="History Key Field"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="History",
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
            ],
        ),
        migrations.CreateModel(
            name="JoinType",
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
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Join Type"
                    ),
                ),
                ("code", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="LogicOperator",
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
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Logic Operator"
                    ),
                ),
                ("code", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Operator",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("code", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="TableType",
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
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Table Type"
                    ),
                ),
                ("code", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="TaskType",
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
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Task Type"
                    ),
                ),
                ("code", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="WriteDisposition",
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
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Write Disposition"
                    ),
                ),
                ("code", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="jobtype",
            name="code",
            field=models.CharField(default="Code", max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="job",
            name="type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.jobtype",
            ),
        ),
        migrations.CreateModel(
            name="Join",
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
                    "left",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Left Table"
                    ),
                ),
                ("right", models.CharField(max_length=255, verbose_name="Right Table")),
                (
                    "type",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="core.jointype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JobTask",
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
                ("name", models.CharField(max_length=255, verbose_name="Task Name")),
                (
                    "destination_table",
                    models.CharField(max_length=255, verbose_name="Destination Table"),
                ),
                (
                    "destination_dataset",
                    models.CharField(
                        max_length=255, verbose_name="Destination Dataset"
                    ),
                ),
                (
                    "driving_table",
                    models.CharField(max_length=255, verbose_name="Driving Table"),
                ),
                (
                    "staging_dataset",
                    models.CharField(max_length=255, verbose_name="Destination Table"),
                ),
                ("properties", models.JSONField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("lastupdate", models.DateTimeField(auto_now=True)),
                (
                    "createdby",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="job_task_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.job"
                    ),
                ),
                (
                    "table_type",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="core.tabletype",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="core.tasktype",
                    ),
                ),
                (
                    "updatedby",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="job_task_updated_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "write_disposition",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="core.writedisposition",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HistoryOrder",
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
                ("is_desc", models.BooleanField()),
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
        migrations.AddField(
            model_name="history",
            name="task",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="core.jobtask"
            ),
        ),
        migrations.AddField(
            model_name="field",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.jobtask"
            ),
        ),
        migrations.CreateModel(
            name="DrivingColumn",
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
        migrations.CreateModel(
            name="Dependency",
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
                    "dependant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dependant",
                        to="core.jobtask",
                    ),
                ),
                (
                    "predecessor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="predecessor",
                        to="core.jobtask",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Delta",
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
                    "lower_bound",
                    models.CharField(max_length=255, verbose_name="Lower Bound"),
                ),
                ("upper_bound", models.IntegerField(null=True)),
                (
                    "field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.field"
                    ),
                ),
                (
                    "task",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="core.jobtask"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ConditionField",
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
                ("field", models.CharField(max_length=255, verbose_name="Field")),
                (
                    "condition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.condition"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="condition",
            name="join",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.join"
            ),
        ),
        migrations.AddField(
            model_name="condition",
            name="logi_operator",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="core.logicoperator",
            ),
        ),
        migrations.AddField(
            model_name="condition",
            name="operator",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="core.operator",
            ),
        ),
        migrations.AddField(
            model_name="condition",
            name="where",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.jobtask",
            ),
        ),
    ]
