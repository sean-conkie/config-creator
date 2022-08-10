# Generated by Django 4.0.5 on 2022-07-26 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0036_remove_join_left_remove_join_right_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="field",
            name="source_table",
            field=models.ForeignKey(
                blank=True,
                help_text="Source for the column, include dataset and table names: <dataset name>.<table name>",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.sourcetable",
                verbose_name="Source Table",
            ),
        ),
    ]
