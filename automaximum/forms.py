from django import forms
from .models import *

class operation_product_cashbox_instanceForm(forms.ModelForm):

    class Meta:
        model = operation_product_cashbox_instance
        fields = ('cashbox', 'operation_product', 'operation_money', 'cash', )
        widgets = {
            'cashbox': forms.Select(attrs={'class': 'form-control'}),
            'operation_product': forms.Select(attrs={'class': 'form-control'}),
            'operation_money': forms.Select(attrs={'class': 'form-control'}),
            'cash': forms.NumberInput(attrs={'class': 'form-control','rows':"3",'placeholder':'Сумма'}),
        }
class operation_product_product_instanceForm(forms.ModelForm):

    class Meta:
        model = operation_product_product_instance
        fields = ('product', 'product_amount', 'product_price',)
        widgets = {
            'product': forms.HiddenInput(attrs={'class': 'form-control','placeholder':'Продукция'}),
            'product_amount': forms.NumberInput(attrs={'class': 'form-control price-gen','placeholder':'Кол-во','style':'padding-right: 0px;padding-left: 2px;'}),
            'product_price': forms.NumberInput(attrs={'class': 'form-control price-gen','placeholder':'Цена','style':'padding-right: 0px;padding-left: 2px;'})
        }

class access_levelForm(forms.ModelForm):

    class Meta:
        model = access_level
        fields = ('name', 'access',)
#cashbox
class cashboxForm(forms.ModelForm):
    
    class Meta:
        model = cashbox
        fields = ('name', 'commentary','admin_cashbox',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
            'commentary': forms.Textarea(attrs={'class': 'form-control','rows':"3",'placeholder':'Примечание'}),
        }
#type_operation_money
class type_operation_moneyForm(forms.ModelForm):
    
    class Meta:
        model = type_operation_money
        fields = ('type', 'name', )
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
        }
#client
class clientForm(forms.ModelForm):
    
    class Meta:
        model = client
        fields = ('name', 'adress', 'number', 'price', 'card', 'supplier',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
            'adress': forms.TextInput(attrs={'class': 'form-control','placeholder':'Адресс'}),
            'number': forms.TextInput(attrs={'class': 'form-control','placeholder':'Номер телефона'}),
            'price': forms.Select(attrs={'class': 'form-control'}),
            'card': forms.TextInput(attrs={'class': 'form-control','placeholder':'Карта'}),
        }        
#type_operation_product
class type_operation_productForm(forms.ModelForm):
    
    class Meta:
        model = type_operation_product
        fields = ('type', 'name', 'default_price', 'default_client', 'creates','changes_price' )
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
            'default_price': forms.Select(attrs={'class': 'form-control'}),
            'default_client': forms.Select(attrs={'class': 'form-control'}),
            'creates': forms.Select(attrs={'class': 'form-control'}),

        }
#storage
class storageForm(forms.ModelForm):
    
    class Meta:
        model = storage
        fields = ('name', 'commentary',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
            'commentary': forms.Textarea(attrs={'class': 'form-control','rows':"3",'placeholder':'Примечание'}),
        }
#price
class priceForm(forms.ModelForm):
    
    class Meta:
        model = price
        fields = ( 'name', 'nacenka','analogue',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
            'nacenka': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Наценка(множитель)'}),
            'analogue': forms.Select(attrs={'class': 'form-control'}),
        }
#operation_product
class operation_productForm(forms.ModelForm):

    class Meta:
        model = operation_product
        fields = ('created_date', 'client', 'storage_recieve', 'created_by', 'commentary', 'storage', 'price', 'car','need_to_edit', 'need_to_edit_commentary')
        widgets = {
            'created_date': forms.DateTimeInput(attrs={'class': 'form-control','placeholder':'Дата'}),
            'client': forms.Select(attrs={'class': 'form-control','placeholder':'Клиент'}),
            'storage_recieve': forms.Select(attrs={'class': 'form-control','placeholder':'Склад получатель'}),
            'created_by': forms.Select(attrs={'class': 'form-control','placeholder':'Создано'}),
            'commentary': forms.Textarea(attrs={'class': 'form-control','rows':"3",'placeholder':'Примечание'}),
            'storage': forms.Select(attrs={'class': 'form-control','placeholder':'Склад'}),
            'price': forms.Select(attrs={'class': 'form-control','placeholder':'Цена'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'need_to_edit_commentary': forms.Textarea(attrs={'class': 'form-control','rows':"3",'placeholder':'Описание для редактирования'}),
        }
        labels = {
            'created_date': ('Дата'),
            'client': ('Клиент'),
            'storage_recieve': ('Склад получатель'),
            'created_by': ('Создано'),
            'commentary': ('Примечание'),
            'storage': ('Склад'),
            'price': ('Цена'),
        }
#car
class carForm(forms.ModelForm):

    class Meta:
        model = car
        fields = ('name', 'subcategory_of', 'engine', 'full_num','date1','date2',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
            'subcategory_of': forms.Select(attrs={'class': 'form-control'}),
            'engine': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'full_num': forms.TextInput(attrs={'class': 'form-control','placeholder':'Полный номер кузова'}),
            'date1': forms.DateInput(attrs={'class': 'form-control','placeholder':'Дата начала выпуска'}),
            'date2': forms.DateInput(attrs={'class': 'form-control','placeholder':'Дата окончания выпуска'}),
}
#manufacturer
class manufacturerForm(forms.ModelForm):

    class Meta:
        model = manufacturer
        fields = ('name', 'commentary', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
            'commentary': forms.Textarea(attrs={'class': 'form-control','rows':"3",'placeholder':'Примечание'}),
        }
#characteristics
class characteristicsForm(forms.ModelForm):

    class Meta:
        model = characteristics
        fields = ('name','type','edinica', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'edinica': forms.TextInput(attrs={'class': 'form-control','placeholder':'Единица измерения'}),
        }
#engine
class engineForm(forms.ModelForm):

    class Meta:
        model = engine
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
        }
#part_of
class part_ofForm(forms.ModelForm):

    class Meta:
        model = part_of
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
        }
#part_of_car
class part_of_carForm(forms.ModelForm):

    class Meta:
        model = part_of_car
        fields = ('part_of',)
        widgets = {
            'part_of': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }        
#category
class categoryForm(forms.ModelForm):

    class Meta:
        model = category
        fields = ('name', 'short_description', 'subcategory_of', 'characteristics', 'useinfullname','characteristics_forname',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control','rows':"3",'placeholder':'Краткое описание'}),
            'subcategory_of': forms.Select(attrs={'class': 'form-control'}),
            'characteristics': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'characteristics_forname': forms.SelectMultiple(attrs={'class': 'form-control'}),
            }
#product
class productForm(forms.ModelForm):

    class Meta:
        model = product
        fields = ('argus_name', 'argus_article', 'article', 'article_alt', 'category', 'manufacturer', 'commentary','need_to_edit', 'need_to_edit_commentary', 'monitor_amount', 'min_amount', 'monitor_price','price0', 'analogue', 'car', 'engine')
        widgets = {
            'argus_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Название по аргусу'}),
            'argus_article': forms.TextInput(attrs={'class': 'form-control','placeholder':'Код по аргусу'}),
            'article': forms.TextInput(attrs={'class': 'form-control','placeholder':'Артикул'}),
            'article_alt': forms.TextInput(attrs={'class': 'form-control','placeholder':'Альтернативный артикул'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'min_amount': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Минимальный остаток'}),
            'manufacturer': forms.Select(attrs={'class': 'form-control'}),
            'commentary': forms.Textarea(attrs={'class': 'form-control','rows':"3",'placeholder':'Текст для описания'}),
            'price0': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Закупочная цена'}),
            'need_to_edit_commentary': forms.TextInput(attrs={'class': 'form-control','placeholder':'Описание для редактирования'}),
}
#price_value
class price_valueForm(forms.ModelForm):

    class Meta:
        model = price_value
        fields = ('value','nacenka',)
        widgets = {
        'value': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Цена'}),
        'nacenka': forms.NumberInput(attrs={'class': 'form-control','rows':"3",'placeholder':'Наценка(множитель)'}),

        }

#characteristics_value
class characteristics_valueForm(forms.ModelForm):

    class Meta:
        model = characteristics_value
        fields = ('value','text', 'choice',)
        widgets = {
            'value': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Значение'}),
            'text': forms.TextInput(attrs={'class': 'form-control','placeholder':'Значение'}),
            'choice': forms.Select(attrs={'class': 'form-control'}),
            }

class characteristics_choicesForm(forms.ModelForm):

    class Meta:
        model = characteristics_choices
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control','placeholder':'Значение'}),
            }
#amount_on_storage
class amount_on_storageForm(forms.ModelForm):

    class Meta:
        model = amount_on_storage
        fields = ('amount',)
#operation money
class operation_moneyForm(forms.ModelForm):

    class Meta:
        model = operation_money
        fields = ('created_date', 'type', 'client', 'cashbox_recieve', 'cash', 'commentary',)
        widgets = {
            'created_date': forms.DateTimeInput(attrs={'class': 'form-control','placeholder':'Дата'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'cashbox_recieve': forms.Select(attrs={'class': 'form-control'}),
            'cash': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Сумма'}),
            'commentary': forms.Textarea(attrs={'class': 'form-control','rows':"3",'placeholder':'Примечание'}),
        }
#user
from django.contrib.auth.models import User
class userForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
#user_profile
class user_profileForm(forms.ModelForm):
    class Meta:
        model = user_profile
        fields = ('name', 'access_level')
