# Generated by Django 2.0.4 on 2018-06-26 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('automaximum', '0004_auto_20180627_0739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='has_article',
        ),
        migrations.AlterField(
            model_name='category',
            name='characteristics',
            field=models.ManyToManyField(blank=True, to='automaximum.characteristics', verbose_name='Характеристики'),
        ),
        migrations.AlterField(
            model_name='category',
            name='characteristics_forname',
            field=models.ManyToManyField(blank=True, related_name='characteristics_forname', to='automaximum.characteristics', verbose_name='Характеристики для названия'),
        ),
        migrations.AlterField(
            model_name='category',
            name='subcategory_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.category', verbose_name='Подкатегория от'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='analogue',
            field=models.ManyToManyField(blank=True, related_name='_product_analogue_+', to='automaximum.product', verbose_name='Аналоги'),
        ),
        migrations.AlterField(
            model_name='product',
            name='argus_article',
            field=models.CharField(blank=True, max_length=128, verbose_name='Код по аргусу'),
        ),
        migrations.AlterField(
            model_name='product',
            name='argus_name',
            field=models.CharField(blank=True, max_length=256, verbose_name='Название по аргусу'),
        ),
        migrations.AlterField(
            model_name='product',
            name='article',
            field=models.CharField(blank=True, max_length=256, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='product',
            name='article_alt',
            field=models.CharField(blank=True, max_length=256, verbose_name='Альтернативный код'),
        ),
        migrations.AlterField(
            model_name='product',
            name='car',
            field=models.ManyToManyField(blank=True, to='automaximum.car', verbose_name='Машини'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='commentary',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='product',
            name='engine',
            field=models.ManyToManyField(blank=True, to='automaximum.engine', verbose_name='Двигатели'),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.manufacturer', verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='product',
            name='used_with',
            field=models.ManyToManyField(blank=True, related_name='_product_used_with_+', to='automaximum.product', verbose_name='Испульзуется с(не использовано'),
        ),
    ]
