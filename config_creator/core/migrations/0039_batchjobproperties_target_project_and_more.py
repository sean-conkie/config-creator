# Generated by Django 4.0.5 on 2022-07-30 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0038_alter_delta_upper_bound_alter_sourcetable_alias"),
    ]

    operations = [
        migrations.AddField(
            model_name="batchjobproperties",
            name="target_project",
            field=models.CharField(
                blank=True,
                help_text="Target project",
                max_length=255,
                null=True,
                verbose_name="Target Project",
            ),
        ),
        migrations.AddField(
            model_name="dagjobproperties",
            name="target_project",
            field=models.CharField(
                blank=True,
                help_text="Target project",
                max_length=255,
                null=True,
                verbose_name="Target Project",
            ),
        ),
    ]
