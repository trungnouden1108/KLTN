# Generated by Django 3.0.3 on 2020-03-14 06:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0026_auto_20200313_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='id_user',
            field=models.CharField(default=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='book',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 14, 13, 57, 43, 800251)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 14, 13, 57, 43, 800251)),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 14, 13, 57, 43, 799252)),
        ),
    ]
