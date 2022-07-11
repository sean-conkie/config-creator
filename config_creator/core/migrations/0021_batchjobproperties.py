# Generated by Django 4.0.5 on 2022-07-11 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_jobtask_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchJobProperties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(help_text='Enter the prefix which will be used for all tasks in this job; i.e. spine__order', max_length=255, verbose_name='Script Name Prefix')),
                ('job', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.job')),
            ],
        ),
    ]
