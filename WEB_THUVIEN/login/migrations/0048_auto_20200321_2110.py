# Generated by Django 3.0.3 on 2020-03-21 14:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0047_auto_20200321_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docgia',
            name='money_user',
        ),
        migrations.AlterField(
            model_name='book',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 10, 24, 641411)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 10, 24, 688314, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 10, 24, 641411)),
        ),
    ]
