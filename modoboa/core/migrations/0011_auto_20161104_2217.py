# Generated by Django 1.9.5 on 2016-11-04 21:17
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20161026_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localconfig',
            name='_parameters',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='user',
            name='_parameters',
            field=models.JSONField(default=dict),
        ),
    ]
