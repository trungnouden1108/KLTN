# Generated by Django 3.0.3 on 2020-02-17 14:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20200217_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 17, 21, 22, 19, 940972)),
        ),
    ]