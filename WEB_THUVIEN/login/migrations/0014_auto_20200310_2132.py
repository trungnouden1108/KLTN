# Generated by Django 3.0.3 on 2020-03-10 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_auto_20200310_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 10, 21, 32, 57, 431141)),
        ),
        migrations.AlterField(
            model_name='book',
            name='image_book',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 10, 21, 32, 57, 430114)),
        ),
    ]
