# Generated by Django 4.2.6 on 2023-11-06 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_rename_after_changedlog_changes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='is_deleted',
        ),
    ]