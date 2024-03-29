# Generated by Django 4.0.5 on 2022-07-29 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0037_alter_field_source_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="delta",
            name="upper_bound",
            field=models.IntegerField(
                blank=True,
                help_text="Input seconds to add to lower_bound, 86400 represents one day",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="sourcetable",
            name="alias",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Table Alias"
            ),
        ),
    ]
