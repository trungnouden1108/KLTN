# Generated by Django 3.0.3 on 2020-03-10 15:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_auto_20200310_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='image_book',
        ),
        migrations.AlterField(
            model_name='book',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 10, 22, 57, 57, 947770)),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 10, 22, 57, 57, 947770)),
        ),
    ]
