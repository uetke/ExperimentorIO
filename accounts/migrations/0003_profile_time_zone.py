# Generated by Django 2.0.6 on 2018-06-06 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180605_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='time_zone',
            field=models.IntegerField(default=0),
        ),
    ]
