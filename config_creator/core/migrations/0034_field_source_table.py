# Generated by Django 4.0.5 on 2022-07-22 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0033_sourcetable_alias_sourcetable_base_alias_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="field",
            name="source_table",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.sourcetable",
                verbose_name="Source Table",
            ),
        ),
    ]