# Generated by Django 4.0.5 on 2022-06-22 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_gitrepository"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="git_username",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
