# Generated by Django 4.0.5 on 2022-06-21 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_alter_conditionfield_condition"),
    ]

    operations = [
        migrations.AlterField(
            model_name="join",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.jobtask"
            ),
        ),
    ]
