# Generated by Django 2.0.6 on 2018-06-08 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_account_expiration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='data_size',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
