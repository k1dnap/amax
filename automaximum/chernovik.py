обновить модели

add users 

https://translate.google.ru/translate?hl=ru&sl=en&u=http://www.tangowithdjango.com/book17/chapters/login.html&prev=search
https://media.readthedocs.org/pdf/tango-with-django/latest/tango-with-django.pdf
https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html


добавить архив


open table on click

http://jsfiddle.net/QLfMU/116/  //jquery
http://jsfiddle.net/whytheday/QLfMU/1/ //css

https://stackoverflow.com/questions/16389775/twitter-bootstrap-use-collapse-js-on-table-cells-almost-done

.distinct() - работа только с уникальными значениями(при куче одинаковых обхектов берет только 1 уник)

users = User.objects.all().select_related('profile') выбирает 



    operation_payment = models.ManyToManyField('operation_money', through='operation_payment',
                        through_fields=('operation_product','operation_money'),)      

'opticalhc.ru'+self.filename.url

 + operation_money.type + 'на сумму ' + operation_money.cash + 'в кассе ' cashbox1


            

http://bootstrap-3.ru/bootstraptheme.php obrazci
    http://bootstrap-3.ru/examples/offcanvas/ s menushkami
    http://bootstrap-3.ru/examples/starter-template/ pustaya
    http://bootstrap-3.ru/examples/sticky-footer-navbar/ footer k botu

ordering = ["horn_length"]

http://www.tangowithdjango.com/book17/chapters/login.html

https://stackoverflow.com/questions/13463399/how-to-design-shopping-basket-using-session

https://stackoverflow.com/questions/48716346/django-cart-and-item-model-getting-quantity-to-update
https://stackoverflow.com/questions/36147597/adding-items-to-shopping-cart-django-python

https://github.com/codingmedved/shop/blob/master/diagram.jpg

https://www.youtube.com/watch?v=c2Q9wj9ju3Y busket

javascript count:
https://www.w3schools.com/howto/howto_js_weight_converter.asp

python3 timeweb
http://timeweb.com/ru/community/articles/kak-ispolzovat-postgresql-c-prilozheniem-django-na-ubuntu-16-04

django gunicorn ngnix
https://habr.com/post/159575/


        https://www.w3schools.com/bootstrap/bootstrap_tabs_pills.asp


oplata product create slomana

создать oplata product на основании исходя из данных в ведре,

создать oplata product на основании исходя из данных в операции продукт

при нажатиивызывается всплывающее окно в котором выбирается тип создаваемой операции, открывается страница с ?query = (operation_product\product in basker user_id)
исходя из инициальных данныхф ормируется операция с initial value 

https://www.w3schools.com/bootstrap/bootstrap_collapse.asp

https://stackoverflow.com/questions/4876462/django-allow-admin-user-to-edit-site-wide-settings
https://stackoverflow.com/questions/1900956/write-variable-to-file-including-name
editformset = editformset1(request.POST, queryset=characteristics_value.objects.filter(product=product1))

    value = models.CharField(max_length=128, blank = True, verbose_name=str(characteristics))
    text = models.CharField(max_length=128, blank = True, verbose_name=str(characteristics))
    choice 






$(this).parent().html("");
$(this).parent().find('ul:last').html("");














<p><label for="id_category">Category:</label> <select name="category" required="" id="id_category">
  <option value="" selected="">---------</option>

  <option value="3">Автохимия</option>

  <option value="1">Детали ходовой части</option>

  <option value="2">Детали ходовой части/Втулки</option>

  <option value="6">Детали ходовой части/Втулки/Полеуретановые</option>

  <option value="9">Детали ходовой части/Втулки/Полеуретановые/полеуретановыенаполовину</option>

  <option value="8">Детали ходовой части/Втулки/Полеуретановые/полуполеуретановые</option>

  <option value="7">Детали ходовой части/Втулки/Резиновые</option>

  <option value="5">Детали ходовой части/Сайлентблок</option>

  <option value="10">Масло</option>
initial={'commentary': 'I love your site!'}

arms['product_amount'].initial = float(zae.value)
form.fields["analogue"].queryset = product.objects.filter(category=product1.category).exclude(pk=product1.pk)
del kkl.fields["value"]
del kkl.fields["text"]
del kkl.fields["choice"]


    types = (
    ('int', 'Число'),
    ('choice', 'Выбор'),
    ('string', 'Текст'),
    )

    form.fields["category"].empty_label=None

    https://docs.djangoproject.com/en/2.0/topics/forms/#rendering-fields-manually
    https://getbootstrap.com/docs/3.3/css/#forms

                fields = list(kkl)
                kkl.part1, kkl.part2,kkl.part3 = fields[0], fields[1],fields[2:]
                fields= None


формы в линии:
https://stackoverflow.com/questions/22888298/bootstrap-3-how-to-get-two-form-inputs-on-one-line-and-other-inputs-on-individu
https://stackoverflow.com/questions/19089901/bootstrap-3-two-forms-on-the-same-line
https://stackoverflow.com/questions/40931791/bootstrap-form-fields-on-the-same-line
https://stackoverflow.com/questions/28786475/how-to-put-multiple-bootstrap-inputs-on-same-line

widgets = {
    'argus_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название по аргусу'}),
    'commentary': forms.Textarea(attrs={'class': 'form-control','rows':"3",'placeholder':'Текст для описания'}),
    'category': forms.Select(attrs={'class': 'form-control'}),
    'commentary': forms.SelectMultiple(attrs={'class': 'form-control'}),
    'commentary': forms.CheckboxInput(attrs={'class': 'form-control'}),
    'commentary': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Текст для описания'}),\\ ещё посмотри целые\нецелые числа
}

fields = ('name', 'subcategory_of', 'engine', 'full_num','date1','date2',)
widgets = {
    'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
    'subcategory_of': forms.Select(attrs={'class': 'form-control'}),
    'engine': forms.Select(attrs={'class': 'form-control'}),
    'full_num': forms.TextInput(attrs={'class': 'form-control','placeholder':'Полный номер кузова'}),
    'date1': forms.DateInput(attrs={'class': 'form-control','placeholder':'Дата начала выпуска'}),
    'date2': forms.DateInput(attrs={'class': 'form-control','placeholder':'Дата окончания выпуска'}),
}