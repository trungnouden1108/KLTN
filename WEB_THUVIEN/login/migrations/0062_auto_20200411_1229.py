# Generated by Django 3.0.3 on 2020-04-11 05:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0061_auto_20200410_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='ave_rate',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='create1',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 11, 12, 29, 13, 894461, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='create2',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 11, 12, 29, 13, 894461, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='create3',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 11, 12, 29, 13, 894461, tzinfo=utc)),
        ),
    ]
