# Generated by Django 4.2.6 on 2023-11-03 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_changedlog_before'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changedlog',
            name='after',
            field=models.JSONField(null=True),
        ),
    ]
