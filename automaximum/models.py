#cashbox hidden bool
#product has article or no
#product is part of
#product canbe used with
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django import forms
from django.contrib.auth.models import User


class trading_product_in_basket(models.Model):
    user = models.ForeignKey(User, blank = False,  on_delete=models.CASCADE)
    product = models.ForeignKey('product', blank = False, on_delete=models.CASCADE)
    value = models.IntegerField(default = 0)
    class Meta:
        ordering = ['product']
    def __str__(self):
        return self.user.username

#доступ
class access(models.Model):
    name = models.CharField(max_length=128, blank = False, unique=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class access_level(models.Model):
    name = models.CharField(max_length=128, blank = False, unique=True)
    access = models.ManyToManyField(access, blank = True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

#пользователь
class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank = False, unique = True)
    access_level = models.ForeignKey('access_level', blank = True, null= True, on_delete=models.SET_NULL )
    access = models.ManyToManyField(access, blank = True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.user.username

#цена
class price(models.Model):
    name = models.CharField(max_length=64, blank = False, unique = True)
    #наценка_фл, используется в предложении формирования цен, (nacenka*price0), по дефолту = 2(200%).
    nacenka = models.FloatField(blank=True, default = 2.0)
    analogue = models.ForeignKey("self", blank=True, null= True, verbose_name='цена от которой считать', on_delete=models.SET_NULL)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

#клиент
class client(models.Model):
    name = models.CharField(max_length=128, blank = False, unique = True, verbose_name='Название')
    adress = models.CharField(max_length=128, blank = True, verbose_name='Адресс')
    number = models.CharField(max_length=32, blank = True, verbose_name='Номер телефона')
    price = models.ForeignKey('price', blank = True, null= True, on_delete=models.SET_NULL, verbose_name='Цена' )
    card = models.CharField(max_length=64, blank = True, verbose_name='Номер карты')
    cash = models.FloatField(default=0)
    created_date = models.DateTimeField(default=timezone.now, verbose_name='дата')
    creator = models.ForeignKey(User, blank = True, null= True, on_delete=models.SET_NULL)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
#касса
class cashbox(models.Model):
    name = models.CharField(max_length=128, blank = False, unique=True, verbose_name='Название')
    cash = models.FloatField(default=0)
    commentary = models.TextField(blank = True, verbose_name='Примечание')
    admin_cashbox = models.BooleanField(default=False, verbose_name='Касса администратора')
    
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

#склад
class storage(models.Model):
    name = models.CharField(max_length=128, blank = False, unique=True, verbose_name='Название')
    commentary = models.TextField(blank = True, verbose_name='Примечание')
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name



#двигатель
class engine(models.Model):
    name = models.CharField(max_length=64, blank = False, unique=True, verbose_name='Название')
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name	

#машина
class car(models.Model):
    name = models.CharField(max_length=128, blank = False, verbose_name='Название')
    full_num = models.CharField(max_length=128, blank = True, verbose_name='Полный номер кузова')
    subcategory_of = models.ForeignKey('self', blank=True, null= True, on_delete=models.SET_NULL, verbose_name='Подкатегория от')
    date1 = models.DateField(blank = True, null= True, default=timezone.now, verbose_name='Дата начала выпуска')
    date2 = models.DateField(blank = True, null= True, default=timezone.now, verbose_name='Дата окончания выпуска')
    engine = models.ManyToManyField(engine, blank = True, verbose_name='Двигатель')
    slug = models.SlugField(blank=True, max_length=128, allow_unicode=True)
    full_name = models.CharField(max_length=128, blank = True)
    class Meta:
        ordering = ['full_name']
    def save(self, *args, **kwargs):
        full_path = [self.name]
        k = self.subcategory_of 
        while k is not None:
            full_path.append(k.name)
            k = k.subcategory_of
        full_name = '/'.join(full_path[::-1])
        self.full_name = full_name
        if self == self.subcategory_of:
            return errors   
        else:
            super().save()
    def __str__(self):
        return self.full_name

#Характеристика
class characteristics(models.Model):
    types = (
    ('int', 'Число'),
    ('choice', 'Выбор'),
    ('string', 'Текст'),
    )
    name = models.CharField(max_length=128, blank = False, unique=True, verbose_name='Название')
    type = models.CharField(max_length=22, blank=False, choices=types, default='int', verbose_name='Вид характеристики')
    edinica = models.CharField(max_length=8, blank = True, verbose_name='Единица измерения')
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
    def get_choices(self):
       return characteristics_choices.objects.filter(characteristics=self)  

class characteristics_choices(models.Model):
    characteristics = models.ForeignKey(characteristics, blank = False,null= True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=128, blank=False, verbose_name='Значение')
    class Meta:
        ordering = ['characteristics']
    def __str__(self):
        return self.text

#категория
class category(models.Model):
    name = models.CharField(max_length=128, blank=False, unique=True, verbose_name='Название')
    slug = models.SlugField(blank=True, max_length=128, allow_unicode=True)
    short_description = models.TextField(blank=True, verbose_name='Краткое описание')
    searchtags = models.TextField(blank=True, verbose_name='Теги для поиска')
 #   mainimg = models.ImageField(upload_to='categories/', blank=True, verbose_name='Изображение')
    subcategory_of = models.ForeignKey('self', blank=True, null= True, on_delete=models.SET_NULL, verbose_name='Подкатегория от')
    characteristics = models.ManyToManyField(characteristics, blank = True, verbose_name='Характеристики')
    full_name = models.CharField(max_length=128, blank = True)
    useinfullname = models.BooleanField(default=True, verbose_name='Использовать в названии')
    characteristics_forname = models.ManyToManyField('characteristics', blank = True, related_name="characteristics_forname", verbose_name='Характеристики в названии названия')
    class Meta:
        ordering = ['full_name']
        verbose_name = ("Категорию")
        verbose_name_plural = ("Категории")
    def get_cat(self):
       return category.objects.filter(subcategory_of=self)     
    def save(self, *args, **kwargs):
        full_path = [self.name]
        k = self.subcategory_of 
        while k is not None:
            full_path.append(k.name)
            k = k.subcategory_of
        full_name = '/'.join(full_path[::-1])
        self.full_name = full_name
        if self == self.subcategory_of:
            return errors   
        else:
            super().save()

    def __str__(self):
        full_path = [self.name]
        k = self.subcategory_of

        while k is not None:
            full_path.append(k.name)
            k = k.subcategory_of

        return '/'.join(full_path[::-1])



#производитель
class manufacturer(models.Model):
    name = models.CharField(max_length=128, blank = False, unique=True, verbose_name='Название')
    commentary = models.TextField(blank = True, verbose_name='Примечание')
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class part_of(models.Model):
    name = models.CharField(max_length=128, blank = False, unique=True, verbose_name='Название')
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name



#продукцияs
class product(models.Model):
    argus_name = models.CharField(max_length=256, blank = True, verbose_name='Название по аргусу')
    argus_article = models.CharField(max_length=128, blank = True, verbose_name='Код по аргусу')
    car = models.ManyToManyField(car, blank = True, verbose_name='Машины')
    engine = models.ManyToManyField(engine, blank = True, verbose_name='Двигатели')   
    category = models.ForeignKey('category', blank=False, null= True, on_delete=models.SET_NULL, verbose_name='Категория')
    article = models.CharField(max_length=256, blank = True, verbose_name='Артикул')
    used_with = models.ManyToManyField("self", blank = True, verbose_name='Испульзуется с(не использовано')
    #часть, к примеру втулка находится в передних верхних рычагах
    #part_of = models.ManyToManyField(part, blank = True)
    analogue = models.ManyToManyField("self", blank=True, verbose_name='Аналоги')
    full_name = models.CharField(max_length=128, blank = True)
    article_alt = models.CharField(max_length=256, blank = True, verbose_name='Альтернативный артикул')
    manufacturer = models.ForeignKey('manufacturer', blank = True, null= True, on_delete=models.SET_NULL, verbose_name='Производитель')
    commentary = models.TextField(blank = True, verbose_name='Описание')
    #approved pri perenose = False, v dalneishem ispolzueyetsya dlya spiska neotredoktirovannykh kartochek
    approved = models.BooleanField(default=True)
    #mozhno li udalit' bez vreda baze dannykh
    deletefree = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    #хар-ки от категории
    characteristics = models.ManyToManyField(characteristics, through='characteristics_value',
                        through_fields=('product','characteristics'),)
    #partofcar
    #part_of = models.ManyToManyField(car, through='part_of_car',
                        #through_fields=('product','car'),)
    #количество на складах
    amount = models.ManyToManyField(storage, through='amount_on_storage',
                        through_fields=('product','storage'),) 
    #всего кол-во
    amount0 = models.FloatField(blank=True, null=True, default = 0, verbose_name='Общее количество')
    #цена
    price = models.ManyToManyField(price, through='price_value',
                        through_fields=('product','price'),) 
    #0 - закуп
    price0 = models.FloatField(blank=True, null=True, default = 0, verbose_name='Закупочная цена')
    class Meta:
        ordering = ['full_name']

    def save(self, *args, **kwargs):
        f_name = []
        if self.category.useinfullname == True:
            f_name.append(self.category.name)
            if self.article != None:
                f_name.append(self.article)
            if self.manufacturer != None:
                f_name.append(self.manufacturer.name)
            if self.id != None:
                if self.category.characteristics_forname != None:
                    klq = characteristics_value.objects.filter(product = self)
                    if klq.exists(): 
                        for samovar in self.category.characteristics_forname.all():
                            dsa = klq.get(characteristics=samovar)
                            print(dsa.value)
                            if dsa.characteristics.type  == 'string' and dsa.text != '':
                                f_name.append(dsa.text)
                                print('mi tut')
                            if dsa.characteristics.type  == 'int' and dsa.value != '':
                                f_name.append(str(dsa.value)+dsa.characteristics.edinica)
                            if dsa.characteristics.type  == 'choice' and dsa.choice != None:
                                f_name.append(dsa.choice.text)
            name_full = ' '.join(f_name[::1])
            self.full_name = name_full
        else:
            if self.article != '':
                if self.manufacturer != None:
                    self.full_name = self.article + ' ' + str(self.manufacturer.name)
                else:
                    self.full_name = self.article
            else:
                self.full_name = self.argus_name
                
        if self.id != None:
            for kiz in self.analogue.all():
                if self == kiz:
                    return errors
        super().save()     

    
    def __str__(self):
        return self.full_name

#dobav' v formi i t'd
class part_of_car(models.Model):
    car = models.ForeignKey(car, blank=True, null= True, on_delete=models.SET_NULL)
    product = models.ForeignKey(product, blank=True, null= True, on_delete=models.SET_NULL)
    engine = models.ForeignKey(engine, blank=True, null= True, on_delete=models.SET_NULL)
    part_of = models.ManyToManyField(part_of, blank=True, verbose_name='Часть автомобиля')
    def __str__(self):
        return str(self.product)


class characteristics_value(models.Model):
    characteristics = models.ForeignKey(characteristics, blank=False, null= True, on_delete=models.SET_NULL)
    product = models.ForeignKey(product, blank=False, null= True, on_delete=models.SET_NULL)
    value = models.FloatField(max_length=128, blank = True, verbose_name=str(characteristics))
    text = models.CharField(max_length=128, blank = True, verbose_name=str(characteristics))
    choice = models.ForeignKey(characteristics_choices, blank = True, null= True, on_delete=models.SET_NULL, verbose_name=str(characteristics))
    class Meta:
        ordering = ['characteristics']
    def __str__(self):
        return str(self.characteristics) + ' ' + str(self.product)

class amount_on_storage(models.Model):
    storage = models.ForeignKey(storage, blank=False, null= True, on_delete=models.SET_NULL)
    product = models.ForeignKey(product, blank=False, null= True, on_delete=models.SET_NULL)
    amount = models.FloatField(blank=True, null=True)
    class Meta:
        ordering = ['storage']
    def __str__(self):
        return str(self.product) + ' ' + str(self.storage)

class price_value(models.Model):
    price = models.ForeignKey(price, blank=False, null= True, on_delete=models.SET_NULL)
    product = models.ForeignKey(product, blank=False, null= True, on_delete=models.SET_NULL)
    value = models.FloatField(blank=True, null=True)
    nacenka = models.FloatField(blank=True, null=True)
    class Meta:
        ordering = ['price']
    def genprice(self):
        modif = self.price.nacenka
        if self.nacenka != None and self.nacenka != 0:
            modif = self.nacenka
        if self.price.analogue == None:
            znach = self.product.price0
        else:
            iud = price_value.objects.get(price=self.price.analogue, product=self.product)
            znach = iud.value
        rethjk = modif * znach
        return rethjk
    def __str__(self):
        return str(self.price) + ' ' + str(self.product)


#вид операция_деньги
class type_operation_money(models.Model):
    types = (
    ('minus', 'Расход'),
    ('plus', 'Приход'),
    ('minusplus', 'Перемещение'),
    )
    type = models.CharField(max_length=22, blank=False, choices=types, default='minus', verbose_name='Вид')
    name = models.CharField(max_length=100, blank = False, unique=True, verbose_name='Название')
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name


#https://stackoverflow.com/questions/881792/how-to-use-dynamic-foreignkey-in-django        
#операция_деньги
class operation_money(models.Model):
    type = models.ForeignKey('type_operation_money', null= True, on_delete=models.SET_NULL)
    client = models.ForeignKey('client', null= True, on_delete=models.SET_NULL, verbose_name='Клиент')
    cashbox = models.ForeignKey('cashbox', blank = True, null= True, on_delete=models.SET_NULL)
    cashbox_recieve = models.ForeignKey('cashbox', blank = True, null= True, on_delete=models.SET_NULL, related_name='cashbox_recieve', verbose_name='Касса-получатель')
    cash = models.FloatField(default = 0, verbose_name='Сумма')
    leftovers = models.FloatField(default = 0)
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    commentary = models.TextField(blank = True, verbose_name='Примечание')
    checked = models.BooleanField(default=False)
    class Meta:
        ordering = ["created_date"]
    def get_cashinstance(self):
       return operation_product_cashbox_instance.objects.filter(operation_money=self)
    def __str__(self):
        return self.type.name



#вид операция_товар
class type_operation_product(models.Model):
    types = (
    ('minus', 'Расход'),
    ('plus', 'Приход'),
    ('minusplus', 'Перемещение'),
    )
    type = models.CharField(max_length=22, blank=False, choices=types, default='minus', verbose_name='Вид')
    name = models.CharField(max_length=100, blank = False, unique=True, verbose_name='Название')
    creates = models.ForeignKey('type_operation_money', blank = True, null= True, on_delete=models.SET_NULL, verbose_name='Создает кассовую операцию')   
    default_price = models.ForeignKey('price', null= True, blank = True, on_delete=models.SET_NULL, verbose_name='Цена по умолчанию')
    default_client = models.ForeignKey('client', null= True, blank = True, on_delete=models.SET_NULL, verbose_name='Клиент по умолчанию')
    changes_price = models.BooleanField(default=False, verbose_name='Изменяет закупочную цену')
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

#операция_товар
class operation_product(models.Model):
    type = models.ForeignKey('type_operation_product', blank = False, null= True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(default=timezone.now, verbose_name='дата')
    client = models.ForeignKey('client', blank = True, null= True, on_delete=models.SET_NULL)
    storage = models.ForeignKey('storage', blank = True, null= True, on_delete=models.SET_NULL)
    storage_recieve = models.ForeignKey('storage', blank = True, null= True, on_delete=models.SET_NULL, related_name='storage_recieve')
    commentary = models.TextField(blank=True)
    cash = models.FloatField(default=0)
    leftovers = models.FloatField(default = 0)
    state = models.IntegerField(default = 0)
    price = models.ForeignKey('price', null= True, blank = True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, blank = True, null= True, on_delete=models.SET_NULL) 
    approved = models.BooleanField(default=False)
    class Meta:
        ordering = ["created_date"]
    def get_prodinstance(self):
       return operation_product_product_instance.objects.filter(operation_product=self)
    def get_cashinstance(self):
       return operation_product_cashbox_instance.objects.filter(operation_product=self)
    def __str__(self):
        return str(self.type)

class operation_product_cashbox_instance(models.Model):
    operation_money = models.ForeignKey(operation_money, blank=True, null= True, on_delete=models.SET_NULL)
    operation_product = models.ForeignKey(operation_product, blank=True, null= True, on_delete=models.SET_NULL)
    cash = models.FloatField(blank=True, null=True, verbose_name='Сумма')
    cashbox = models.ForeignKey('cashbox', blank = True, null= True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(default=timezone.now, verbose_name='дата')
    approved = models.BooleanField(default=False)
    class Meta:
        ordering = ["created_date"]
    def __str__(self):
        return str(self.cash)
        
class operation_product_product_instance(models.Model):
    product = models.ForeignKey(product, blank=True, null= True, on_delete=models.SET_NULL)
    operation_product = models.ForeignKey(operation_product, blank=False, null= True, on_delete=models.SET_NULL)
    product_amount = models.FloatField(blank=True, null=True, verbose_name='Кол-во')
    product_price = models.FloatField(blank=True, null=True, verbose_name='Цена за ед.')
    storage = models.ForeignKey('storage', blank = False, null= True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(default=timezone.now, verbose_name='дата')
    approved = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_date']
    def totalprice(self):
       return (self.product_amount * self.product_price)
    def __str__(self):
        return str(self.product)

#архив
class memory_action(models.Model):
    name = models.CharField(max_length=100, blank = False)
    action = models.TextField(blank = False)
    created_date = models.DateTimeField(default=timezone.now, verbose_name='дата')
    class Meta:
        ordering = ["created_date"]
    def __str__(self):
        return self.name
#
#
#
#
#
#
#class category(models.Model):		
#    title = models.CharField(max_length=200, blank=False, unique=True, verbose_name='Название')
#    slug = models.SlugField(blank=True, max_length=50, allow_unicode=True)
#	
#
#class carousel(models.Model):
#    text = models.IntegerField(verbose_name='Порядковый номер (от 0)')
#    title = models.CharField(max_length=30, blank=True, verbose_name='Название')
#    description = models.CharField(max_length=30, blank=True, verbose_name='Описание')
#    mainimg = models.ImageField(upload_to='carousel/', verbose_name='Изображение')
#    def __str__(self):
#        return str(self.text)
#
#class images(models.Model):
#    placing = (
#    ('main/about_us', 'main/about_us'),
#    ('main/contacts', 'main/contacts'),
#    ('main/products', 'main/products'),
#    ('about_us/main', 'about_us/main'),
#	('products/main', 'products/main'),
#    )
#    showplace = models.CharField(max_length=22, blank=False, choices=placing, default='main/about_us', unique=True, verbose_name='Отображать в')
#    mainimg = models.ImageField(upload_to='images/', verbose_name='Изображение')
#    def __str__(self):
#        return self.showplace
#
#class certificates(models.Model):
#    text = models.IntegerField(verbose_name='Порядковый номер (от 0)')
#    mainimg = models.ImageField(upload_to='certificates/', blank=False, verbose_name='Изображение')
#    class Meta:
#        verbose_name = ("Сертификат")
#        verbose_name_plural = ("Сертификаты")
#    def __str__(self):
#        return str(self.text)
#
#
#class about(models.Model):
#    text = models.TextField(verbose_name='Текст')
#    def __str__(self):
#        return self.text
#    class Meta:
#        verbose_name = ("О компании")
#        verbose_name_plural = ("О компании")
#class contact(models.Model):
#    text = models.TextField(verbose_name='Текст')
#    def __str__(self):
#        return self.text
#    class Meta:
#        verbose_name = ("Контакт")
#        verbose_name_plural = ("Контакты")
#class news(models.Model):
#    name = models.CharField(max_length=200, verbose_name='Имя')
#    number = models.TextField(blank=True, null=True, verbose_name='Номер')
#    created_date = models.DateTimeField(
#            default=timezone.now, verbose_name='дата')
#    email = models.CharField(max_length=200, verbose_name='Емейл')
#    text = models.CharField(max_length=200, verbose_name='Текст')
#    class Meta:
#        verbose_name = ("Обращение")
#        verbose_name_plural = ("Обращения")
#    def publish(self):
#        self.created_date = timezone.now()
#        self.save()
#
#    def __str__(self):
#        return self.name
#
#class category(models.Model):
#    title = models.CharField(max_length=200, blank=False, unique=True, verbose_name='Название')
#    slug = models.SlugField(blank=True, max_length=50, allow_unicode=True)
#    short_description = models.TextField(blank=True, null=True, max_length=200, verbose_name='Краткое описание')
#    searchtags = models.CharField(max_length=200, blank=True, verbose_name='Теги для поиска')
#    mainimg = models.ImageField(upload_to='categories/', blank=True, verbose_name='Изображение')
#    subcategory = models.ForeignKey('self', blank=True, null=True, verbose_name='Подкат', on_delete=models.CASCADE)
#    class Meta:
#        unique_together = ('slug', 'subcategory',)
#        verbose_name = ("Категорию")
#        verbose_name_plural = ("Категории")
#    def get_cat(self):
#       return category.objects.filter(subcategory=self)     
#    def save(self, *args, **kwargs):
#        self.slug = slugify(self.title, allow_unicode=True)
#        if self != self.subcategory:
#            super().save()
#        else:
#            return errors
#    def __str__(self):
#        full_path = [self.title]
#        k = self.subcategory 
#
#        while k is not None:
#            full_path.append(k.title)
#            k = k.subcategory 
#
#        return ' -> '.join(full_path[::-1])
#class product(models.Model):
#    category = models.ForeignKey(category, verbose_name='Категория')
#    title = models.CharField(max_length=200, blank=False, unique=True, verbose_name='Название')
#    slugprod = models.SlugField(blank=True, max_length=50, allow_unicode=True)
#    slugcat = models.SlugField(blank=True, max_length=50, allow_unicode=True)
#    text = models.TextField(blank=True, null=True)
#    short_description = models.TextField(blank=True, null=True, max_length=200, verbose_name='Краткое описание')
#    searchtags = models.CharField(max_length=200, blank=True, verbose_name='Теги для поиска')
#    mainimg = models.ImageField(upload_to='products/', blank=True,  verbose_name='Изображение')
#
#    class Meta:
#        verbose_name = ("Продукцию")
#        verbose_name_plural = ("Продукция")
#    def save(self, *args, **kwargs):
#        self.slugprod = slugify(self.title, allow_unicode=True)
#        self.slugcat = slugify(self.category, allow_unicode=True)
#        super().save()
#    def get_products(self):
#       product.objects.filter(category=self)     
#    def __str__(self):
#        return self.title
#
#class uploads(models.Model):
#    filename = models.FileField(upload_to='uploads/', blank=False, 
#verbose_name='Файл')
#    class Meta:
#        verbose_name = ("Загрузку")
#       verbose_name_plural = ("Загрузки")
#    def __str__(self):
#        return 'opticalhc.ru'+self.filename.url
