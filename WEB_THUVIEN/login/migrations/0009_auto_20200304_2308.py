# Generated by Django 3.0.3 on 2020-03-04 16:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20200304_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='id_book',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='book',
            name='image_book',
            field=models.ImageField(default=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='id_DG',
            field=models.CharField(default='', max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='docgia',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 4, 23, 8, 33, 683536)),
        ),
    ]