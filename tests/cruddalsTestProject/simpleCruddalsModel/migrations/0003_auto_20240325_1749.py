# Generated by Django 3.2.20 on 2024-03-25 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpleCruddalsModel', '0002_auto_20240325_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelc',
            name='char_field',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='modelc',
            name='integer_field',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='modelc',
            name='many_to_many_field',
            field=models.ManyToManyField(blank=True, related_name='many_to_many_C_related', to='simpleCruddalsModel.ModelD'),
        ),
    ]
