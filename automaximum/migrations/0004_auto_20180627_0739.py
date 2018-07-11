# Generated by Django 2.0.4 on 2018-06-26 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('automaximum', '0003_auto_20180624_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='type_operation_product',
            name='changes_price',
            field=models.BooleanField(default=False, verbose_name='Изменяет закупочную цену'),
        ),
        migrations.RemoveField(
            model_name='price',
            name='analogue',
        ),
        migrations.AddField(
            model_name='price',
            name='analogue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.price', verbose_name='цена от которой считать'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amount0',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Общее количество'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price0',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Закупочная цена'),
        ),
    ]
