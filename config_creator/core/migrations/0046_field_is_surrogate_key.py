# Generated by Django 4.0.5 on 2022-10-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0045_auto_20221001_2254"),
    ]

    operations = [
        migrations.AddField(
            model_name="field",
            name="is_surrogate_key",
            field=models.BooleanField(
                default=False, verbose_name="Surrogate Key Field"
            ),
        ),
    ]
