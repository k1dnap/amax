# Generated by Django 2.0.4 on 2018-07-19 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='access_level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('access', models.ManyToManyField(blank=True, to='automaximum.access')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='amount_on_storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, null=True)),
            ],
            options={
                'ordering': ['storage'],
            },
        ),
        migrations.CreateModel(
            name='car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('full_num', models.CharField(blank=True, max_length=128, verbose_name='Полный номер кузова')),
                ('date1', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата начала выпуска')),
                ('date2', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата окончания выпуска')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=128)),
                ('full_name', models.CharField(blank=True, max_length=128)),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='cashbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название')),
                ('cash', models.FloatField(default=0)),
                ('commentary', models.TextField(blank=True, verbose_name='Примечание')),
                ('admin_cashbox', models.BooleanField(default=False, verbose_name='Касса администратора')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=128)),
                ('short_description', models.TextField(blank=True, verbose_name='Краткое описание')),
                ('searchtags', models.TextField(blank=True, verbose_name='Теги для поиска')),
                ('full_name', models.CharField(blank=True, max_length=128)),
                ('useinfullname', models.BooleanField(default=True, verbose_name='Использовать в названии')),
            ],
            options={
                'verbose_name_plural': 'Категории',
                'ordering': ['full_name'],
                'verbose_name': 'Категорию',
            },
        ),
        migrations.CreateModel(
            name='characteristics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название')),
                ('type', models.CharField(choices=[('int', 'Число'), ('choice', 'Выбор'), ('string', 'Текст')], default='int', max_length=22, verbose_name='Вид характеристики')),
                ('edinica', models.CharField(blank=True, max_length=8, verbose_name='Единица измерения')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='characteristics_choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=128, verbose_name='Значение')),
                ('characteristics', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.characteristics')),
            ],
            options={
                'ordering': ['characteristics'],
            },
        ),
        migrations.CreateModel(
            name='characteristics_value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(blank=True, max_length=128, null=True, verbose_name='<django.db.models.fields.related.ForeignKey>')),
                ('text', models.CharField(blank=True, max_length=128, null=True, verbose_name='<django.db.models.fields.related.ForeignKey>')),
                ('characteristics', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.characteristics')),
                ('choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.characteristics_choices', verbose_name='<django.db.models.fields.related.ForeignKey>')),
            ],
            options={
                'ordering': ['characteristics'],
            },
        ),
        migrations.CreateModel(
            name='client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название')),
                ('adress', models.CharField(blank=True, max_length=128, verbose_name='Адрес')),
                ('number', models.CharField(blank=True, max_length=32, verbose_name='Номер телефона')),
                ('card', models.CharField(blank=True, max_length=64, verbose_name='Номер карты')),
                ('cash', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата')),
                ('supplier', models.BooleanField(default=False, verbose_name='Поставщик')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='engine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название')),
                ('commentary', models.TextField(blank=True, verbose_name='Примечание')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='memory_action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('action', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата')),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
        migrations.CreateModel(
            name='operation_money',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.FloatField(default=0, verbose_name='Сумма')),
                ('leftovers', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('commentary', models.TextField(blank=True, verbose_name='Примечание')),
                ('checked', models.BooleanField(default=False)),
                ('cashbox', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.cashbox')),
                ('cashbox_recieve', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cashbox_recieve', to='automaximum.cashbox', verbose_name='Касса-получатель')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.client', verbose_name='Клиент')),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
        migrations.CreateModel(
            name='operation_product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата')),
                ('commentary', models.TextField(blank=True)),
                ('cash', models.FloatField(default=0)),
                ('leftovers', models.FloatField(default=0)),
                ('state', models.IntegerField(default=0)),
                ('approved', models.BooleanField(default=False)),
                ('need_to_edit', models.BooleanField(default=False, verbose_name='Пометка на редактирование')),
                ('need_to_edit_commentary', models.CharField(blank=True, max_length=256, verbose_name='Описание для редактирования')),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.car', verbose_name='Автомобиль')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.client')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
        migrations.CreateModel(
            name='operation_product_cashbox_instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.FloatField(blank=True, null=True, verbose_name='Сумма')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата')),
                ('approved', models.BooleanField(default=False)),
                ('cashbox', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.cashbox')),
                ('operation_money', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.operation_money')),
                ('operation_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.operation_product')),
            ],
            options={
                'ordering': ['created_date'],
            },
        ),
        migrations.CreateModel(
            name='operation_product_product_instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_amount', models.FloatField(blank=True, null=True, verbose_name='Кол-во')),
                ('product_price', models.FloatField(blank=True, null=True, verbose_name='Цена за ед.')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата')),
                ('approved', models.BooleanField(default=False)),
                ('operation_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.operation_product')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='part_of',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='part_of_car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.car')),
                ('engine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.engine')),
                ('part_of', models.ManyToManyField(blank=True, to='automaximum.part_of', verbose_name='Часть автомобиля')),
            ],
        ),
        migrations.CreateModel(
            name='price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название')),
                ('nacenka', models.FloatField(blank=True, default=2.0, verbose_name='Наценка')),
                ('analogue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.price', verbose_name='Цена от которой считать')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='price_value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(blank=True, null=True)),
                ('nacenka', models.FloatField(blank=True, null=True)),
                ('recomend_price', models.FloatField(blank=True, null=True)),
                ('monitor_price', models.BooleanField(default=True, verbose_name='Отслеживать цену')),
                ('price', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.price')),
            ],
            options={
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('argus_name', models.CharField(blank=True, max_length=256, verbose_name='Название по аргусу')),
                ('argus_article', models.CharField(blank=True, max_length=128, verbose_name='Код по аргусу')),
                ('article', models.CharField(blank=True, max_length=256, verbose_name='Артикул')),
                ('full_name', models.CharField(blank=True, max_length=128)),
                ('article_alt', models.CharField(blank=True, max_length=256, verbose_name='Альтернативный артикул')),
                ('commentary', models.TextField(blank=True, verbose_name='Описание')),
                ('approved', models.BooleanField(default=True)),
                ('deletefree', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
                ('edited', models.BooleanField(default=False)),
                ('need_to_edit', models.BooleanField(default=False, verbose_name='Пометка на редактирование')),
                ('need_to_edit_commentary', models.CharField(blank=True, max_length=256, verbose_name='Описание для редактирования')),
                ('monitor_amount', models.BooleanField(default=True, verbose_name='Отслеживать остаток')),
                ('min_amount', models.FloatField(blank=True, default=2, null=True, verbose_name='Минимальный остаток для отслеживания')),
                ('monitor_price', models.BooleanField(default=True, verbose_name='Отслеживать цену')),
                ('amount0', models.FloatField(blank=True, default=0, null=True, verbose_name='Общее количество')),
                ('price0', models.FloatField(blank=True, default=0, null=True, verbose_name='Закупочная цена')),
            ],
            options={
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название')),
                ('commentary', models.TextField(blank=True, verbose_name='Примечание')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='trading_product_in_basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='automaximum.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['product'],
            },
        ),
        migrations.CreateModel(
            name='type_operation_money',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('minus', 'Расход'), ('plus', 'Приход'), ('minusplus', 'Перемещение')], default='minus', max_length=22, verbose_name='Вид')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='type_operation_product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('minus', 'Расход'), ('plus', 'Приход'), ('minusplus', 'Перемещение')], default='minus', max_length=22, verbose_name='Вид')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('changes_price', models.BooleanField(default=False, verbose_name='Изменяет закупочную цену')),
                ('creates', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.type_operation_money', verbose_name='Создает кассовую операцию')),
                ('default_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.client', verbose_name='Клиент по умолчанию')),
                ('default_price', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.price', verbose_name='Цена по умолчанию')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='user_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('access', models.ManyToManyField(blank=True, to='automaximum.access')),
                ('access_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.access_level')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.ManyToManyField(through='automaximum.amount_on_storage', to='automaximum.storage'),
        ),
        migrations.AddField(
            model_name='product',
            name='analogue',
            field=models.ManyToManyField(blank=True, related_name='_product_analogue_+', to='automaximum.product', verbose_name='Аналоги'),
        ),
        migrations.AddField(
            model_name='product',
            name='car',
            field=models.ManyToManyField(blank=True, to='automaximum.car', verbose_name='Машины'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='product',
            name='characteristics',
            field=models.ManyToManyField(through='automaximum.characteristics_value', to='automaximum.characteristics'),
        ),
        migrations.AddField(
            model_name='product',
            name='engine',
            field=models.ManyToManyField(blank=True, to='automaximum.engine', verbose_name='Двигатели'),
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.manufacturer', verbose_name='Производитель'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.ManyToManyField(through='automaximum.price_value', to='automaximum.price'),
        ),
        migrations.AddField(
            model_name='product',
            name='used_with',
            field=models.ManyToManyField(blank=True, related_name='_product_used_with_+', to='automaximum.product', verbose_name='Испульзуется с(не использовано'),
        ),
        migrations.AddField(
            model_name='price_value',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.product'),
        ),
        migrations.AddField(
            model_name='part_of_car',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.product'),
        ),
        migrations.AddField(
            model_name='operation_product_product_instance',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.product'),
        ),
        migrations.AddField(
            model_name='operation_product_product_instance',
            name='storage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.storage'),
        ),
        migrations.AddField(
            model_name='operation_product',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.price'),
        ),
        migrations.AddField(
            model_name='operation_product',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.storage'),
        ),
        migrations.AddField(
            model_name='operation_product',
            name='storage_recieve',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='storage_recieve', to='automaximum.storage'),
        ),
        migrations.AddField(
            model_name='operation_product',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.type_operation_product'),
        ),
        migrations.AddField(
            model_name='operation_money',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.type_operation_money'),
        ),
        migrations.AddField(
            model_name='client',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.price', verbose_name='Цена'),
        ),
        migrations.AddField(
            model_name='characteristics_value',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.product'),
        ),
        migrations.AddField(
            model_name='category',
            name='characteristics',
            field=models.ManyToManyField(blank=True, to='automaximum.characteristics', verbose_name='Характеристики'),
        ),
        migrations.AddField(
            model_name='category',
            name='characteristics_forname',
            field=models.ManyToManyField(blank=True, related_name='characteristics_forname', to='automaximum.characteristics', verbose_name='Характеристики в названии названия'),
        ),
        migrations.AddField(
            model_name='category',
            name='subcategory_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.category', verbose_name='Подкатегория от'),
        ),
        migrations.AddField(
            model_name='car',
            name='engine',
            field=models.ManyToManyField(blank=True, to='automaximum.engine', verbose_name='Двигатель'),
        ),
        migrations.AddField(
            model_name='car',
            name='subcategory_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.car', verbose_name='Подкатегория от'),
        ),
        migrations.AddField(
            model_name='amount_on_storage',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.product'),
        ),
        migrations.AddField(
            model_name='amount_on_storage',
            name='storage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='automaximum.storage'),
        ),
    ]
