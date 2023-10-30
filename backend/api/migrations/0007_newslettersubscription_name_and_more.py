# Generated by Django 4.2.6 on 2023-10-30 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_newslettersubscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslettersubscription',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='newslettersubscription',
            name='subscriber',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.guest'),
        ),
    ]
