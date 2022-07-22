# Generated by Django 4.0.5 on 2022-07-21 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0030_alter_field_data_type_alter_field_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="field",
            name="data_type",
            field=models.ForeignKey(
                blank=True,
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="core.bigquerydatatype",
                verbose_name="Data Type",
            ),
        ),
        migrations.AlterField(
            model_name="field",
            name="position",
            field=models.IntegerField(
                blank=True,
                default=-1,
                help_text="Enter the column's position within the target table",
                verbose_name="Ordinal Position",
            ),
        ),
    ]
