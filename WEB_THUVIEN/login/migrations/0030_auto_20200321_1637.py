# Generated by Django 3.0.3 on 2020-03-21 09:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0029_auto_20200321_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 16, 36, 59, 713511)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 9, 36, 59, 714513, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 16, 36, 59, 712514)),
        ),
    ]
