# Generated by Django 4.2.6 on 2023-10-30 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_newslettersubscription_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newslettersubscription',
            old_name='subscriber',
            new_name='guest_id',
        ),
    ]
