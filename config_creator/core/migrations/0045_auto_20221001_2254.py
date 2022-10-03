# Generated by Django 4.0.5 on 2022-10-01 21:54

from django.db import migrations


def createtasktypedata(apps, schema_editor):
    model = apps.get_model("core", "TaskType")

    if not model.objects.filter(
        name="Truncate Table",
        code="TRUNCATETABLE",
    ).exists():
        model(
            name="Truncate Table",
            code="TRUNCATETABLE",
        ).save()

    if not model.objects.filter(
        name="Custom",
        code="CUSTOM",
    ).exists():
        model(
            name="Custom",
            code="CUSTOM",
        ).save()


def createtasktowritedispositiondata(apps, schema_editor):
    write_disposition = apps.get_model("core", "WriteDisposition")
    task_type = apps.get_model("core", "TaskType")
    map = apps.get_model("core", "TaskTypeToWriteDisposition")

    if not task_type.objects.filter(
        name="Create Table",
        code="CREATETABLE",
    ).exists():
        task_type(
            name="Create Table",
            code="CREATETABLE",
        ).save()

    create_table = task_type.objects.get(
        name="Create Table",
        code="CREATETABLE",
    )

    if not task_type.objects.filter(
        name="Truncate Table",
        code="TRUNCATETABLE",
    ).exists():
        task_type(
            name="Truncate Table",
            code="TRUNCATETABLE",
        ).save()

    truncate_table_task = task_type.objects.get(
        name="Truncate Table",
        code="TRUNCATETABLE",
    )

    if not task_type.objects.filter(
        name="Custom",
        code="CUSTOM",
    ).exists():
        task_type(
            name="Custom",
            code="CUSTOM",
        ).save()

    custom = task_type.objects.get(
        name="Custom",
        code="CUSTOM",
    )

    if not write_disposition.objects.filter(
        name="Write Truncate",
        code="WRITETRUNCATE",
    ).exists():
        write_disposition(
            name="Write Truncate",
            code="WRITETRUNCATE",
        ).save()

    write_truncate = write_disposition.objects.get(
        name="Write Truncate",
        code="WRITETRUNCATE",
    )

    if not write_disposition.objects.filter(
        name="Truncate Table",
        code="DELETE",
    ).exists():
        write_disposition(
            name="Truncate Table",
            code="DELETE",
        ).save()

    truncate_table = write_disposition.objects.get(
        name="Truncate Table",
        code="DELETE",
    )

    if not write_disposition.objects.filter(
        name="Write Append",
        code="WRITEAPPEND",
    ).exists():
        write_disposition(
            name="Write Append",
            code="WRITEAPPEND",
        ).save()

    write_append = write_disposition.objects.get(
        name="Write Append",
        code="WRITEAPPEND",
    )

    if not write_disposition.objects.filter(
        name="Write Transient",
        code="WRITETRANSIENT",
    ).exists():
        write_disposition(
            name="Write Transient",
            code="WRITETRANSIENT",
        ).save()

    write_transient = write_disposition.objects.get(
        name="Write Transient",
        code="WRITETRANSIENT",
    )

    if not map.objects.filter(
        task_type=create_table,
        write_disposition=write_append,
    ).exists():
        map(
            task_type=create_table,
            write_disposition=write_append,
        ).save()

    if not map.objects.filter(
        task_type=create_table,
        write_disposition=write_transient,
    ).exists():
        map(
            task_type=create_table,
            write_disposition=write_transient,
        ).save()

    if not map.objects.filter(
        task_type=create_table,
        write_disposition=write_truncate,
    ).exists():
        map(
            task_type=create_table,
            write_disposition=write_truncate,
        ).save()

    if not map.objects.filter(
        task_type=custom,
        write_disposition=write_truncate,
    ).exists():
        map(
            task_type=custom,
            write_disposition=write_truncate,
        ).save()

    if not map.objects.filter(
        task_type=truncate_table_task,
        write_disposition=truncate_table,
    ).exists():
        map(
            task_type=truncate_table_task,
            write_disposition=truncate_table,
        ).save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0044_alter_batchcustomjobtaskproperties_sql_and_more"),
    ]

    operations = [
        migrations.RunPython(createtasktypedata),
        migrations.RunPython(createtasktowritedispositiondata),
    ]
