# Generated by Django 2.0.4 on 2018-07-15 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automaximum', '0013_product_monitor_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='price_value',
            name='recomend_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
