# Generated by Django 2.0.6 on 2018-06-07 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experimentor', '0005_auto_20180606_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='slug',
            field=models.CharField(max_length=140, null=True),
        ),
    ]
