# Generated by Django 3.0.3 on 2020-03-21 14:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0040_auto_20200321_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 4, 12, 574323)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 4, 12, 621190, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='money',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 4, 12, 574323)),
        ),
    ]
