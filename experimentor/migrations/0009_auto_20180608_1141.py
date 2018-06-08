# Generated by Django 2.0.6 on 2018-06-08 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experimentor', '0008_auto_20180607_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signal',
            name='value_type',
            field=models.PositiveIntegerField(choices=[(1, 'string'), (2, 'bool'), (3, 'float'), (4, 'integer'), (5, 'status'), (6, '1D array'), (7, '2D array')], default=1),
        ),
    ]
