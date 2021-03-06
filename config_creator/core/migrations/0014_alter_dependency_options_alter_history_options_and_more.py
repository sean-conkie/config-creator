# Generated by Django 4.0.5 on 2022-06-26 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_alter_delta_upper_bound_alter_jobtask_properties"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dependency",
            options={"verbose_name": "Dependencie"},
        ),
        migrations.AlterModelOptions(
            name="history",
            options={"verbose_name": "Historie"},
        ),
        migrations.AddField(
            model_name="operator",
            name="symbol",
            field=models.CharField(default="None", max_length=255, unique=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="jobtask",
            name="table_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="core.tabletype",
                verbose_name="Target Table Type",
            ),
        ),
        migrations.AlterField(
            model_name="jobtask",
            name="type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="core.tasktype",
                verbose_name="Task Type",
            ),
        ),
        migrations.AlterField(
            model_name="jobtask",
            name="write_disposition",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="core.writedisposition",
                verbose_name="Write Disposition",
            ),
        ),
    ]
