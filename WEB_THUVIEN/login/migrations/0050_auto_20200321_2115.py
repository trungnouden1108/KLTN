# Generated by Django 3.0.3 on 2020-03-21 14:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0049_auto_20200321_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocGia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_DG', models.CharField(default='', max_length=8)),
                ('ten_DG', models.CharField(max_length=100)),
                ('gioitinh', models.IntegerField(choices=[(0, 'Nữ'), (1, 'Nam')], default=0)),
                ('email_DG', models.EmailField(max_length=200)),
                ('CMND', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('money_user', models.IntegerField(blank=True, default=0)),
                ('time_create', models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 15, 1, 159747))),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='time_create',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 15, 1, 159747)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 21, 21, 15, 1, 222230, tzinfo=utc)),
        ),
    ]
