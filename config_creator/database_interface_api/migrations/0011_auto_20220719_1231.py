# Generated by Django 4.0.5 on 2022-07-19 11:31

from django.db import migrations


def createjobtypesdata(apps, schema_editor):
    model = apps.get_model("database_interface_api", "ConnectionType")

    if not model.objects.filter(
        description="BigQuery",
    ).exists():
        model(
            description="BigQuery",
        ).save()


class Migration(migrations.Migration):

    dependencies = [
        ("database_interface_api", "0010_alter_connection_port"),
    ]

    operations = [migrations.RunPython(createjobtypesdata)]
