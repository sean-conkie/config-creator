# Generated by Django 4.0.5 on 2022-06-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_jobtotasktype"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobtype",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="jointype",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="logicoperator",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="operator",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tabletype",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tasktype",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="writedisposition",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="properties",
            field=models.JSONField(blank=True, null=True),
        ),
    ]