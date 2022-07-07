# Generated by Django 4.0.5 on 2022-06-22 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_user_staff"),
    ]

    operations = [
        migrations.CreateModel(
            name="GitRepository",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField(max_length=250, verbose_name="Repository URL")),
                ("name", models.CharField(max_length=250)),
                (
                    "secret_key",
                    models.CharField(
                        blank=True, max_length=250, null=True, unique=True
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]