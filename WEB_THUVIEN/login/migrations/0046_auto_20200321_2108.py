# Generated by Django 3.0.3 on 2020-03-21 14:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0045_auto_20200321_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 8, 48, 734992)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 8, 48, 789844, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 8, 48, 734992)),
        ),
    ]