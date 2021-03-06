# Generated by Django 3.0.3 on 2020-04-04 07:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0056_auto_20200403_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='created_at',
        ),
        migrations.AddField(
            model_name='cart',
            name='create1',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 4, 14, 56, 4, 791902, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='cart',
            name='create2',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 4, 14, 56, 4, 791902, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='cart',
            name='create3',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 4, 14, 56, 4, 791902, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='book',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
