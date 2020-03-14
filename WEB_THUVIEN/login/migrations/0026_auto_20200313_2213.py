# Generated by Django 3.0.3 on 2020-03-13 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0025_auto_20200313_2206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='book',
        ),
        migrations.AddField(
            model_name='cart',
            name='id_bor',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='book',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 13, 22, 13, 38, 329792)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 13, 22, 13, 38, 330792)),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 13, 22, 13, 38, 328799)),
        ),
    ]
