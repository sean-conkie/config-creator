# Generated by Django 4.0.5 on 2022-07-12 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0025_bigquerydatatype_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="field",
            name="is_nullable",
            field=models.BooleanField(default=True, verbose_name="Is Column Nullable"),
        ),
    ]
