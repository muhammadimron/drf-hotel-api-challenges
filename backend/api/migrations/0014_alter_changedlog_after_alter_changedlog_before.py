# Generated by Django 4.2.6 on 2023-11-03 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_rename_user_changedlog_changed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changedlog',
            name='after',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='changedlog',
            name='before',
            field=models.JSONField(),
        ),
    ]