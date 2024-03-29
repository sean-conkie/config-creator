# Generated by Django 4.0.5 on 2022-07-23 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0034_field_source_table"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="field",
            name="source_name",
        ),
        migrations.AddField(
            model_name="join",
            name="left_table",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="left_table",
                to="core.sourcetable",
                verbose_name="Left Table",
            ),
        ),
        migrations.AddField(
            model_name="join",
            name="right_table",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="right_table",
                to="core.sourcetable",
                verbose_name="Right Table",
            ),
        ),
        migrations.AlterField(
            model_name="field",
            name="source_table",
            field=models.ForeignKey(
                blank=True,
                default=1,
                help_text="Source for the column, include dataset and table names: <dataset name>.<table name>",
                on_delete=django.db.models.deletion.CASCADE,
                to="core.sourcetable",
                verbose_name="Source Table",
            ),
            preserve_default=False,
        ),
    ]
