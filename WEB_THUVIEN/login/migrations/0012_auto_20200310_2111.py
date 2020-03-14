# Generated by Django 3.0.3 on 2020-03-10 14:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_auto_20200310_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='price',
        ),
        migrations.RemoveField(
            model_name='category_book',
            name='description',
        ),
        migrations.RemoveField(
            model_name='category_book',
            name='slug',
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 10, 21, 11, 10, 710941)),
        ),
        migrations.DeleteModel(
            name='Variation',
        ),
    ]
