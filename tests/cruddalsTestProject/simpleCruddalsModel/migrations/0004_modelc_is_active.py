# Generated by Django 3.2.20 on 2024-03-25 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpleCruddalsModel', '0003_auto_20240325_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelc',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
