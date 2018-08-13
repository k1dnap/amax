from django.shortcuts import render, get_object_or_404, redirect, render_to_response, HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.forms import modelformset_factory
from .models import *
from .forms import *
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse

characteristics_mm = characteristics.objects.all()
manufacturer_mm = manufacturer.objects.all()
category_mm = category.objects.all()
engine_mm = engine.objects.all()
car_mm = car.objects.all()
access_level_mm = access_level.objects.all()
price_mm = price.objects.all()
storage_mm = storage.objects.all()
client_mm = client.objects.all()
cashbox_mm = cashbox.objects.all()
type_operation_money_mm = type_operation_money.objects.all()
type_operation_product_mm = type_operation_product.objects.all()
product_mm = product.objects.all()
operation_product_mm = operation_product.objects.all()
operation_money_mm = operation_money.objects.all()
operation_product_product_instance_mm = operation_product_product_instance.objects.all()
operation_product_cashbox_instance_mm = operation_product_cashbox_instance.objects.all()
part_of_mm = part_of.objects.all()
#util
#eto dlya polucheniya tovarov v podkategorii v poiske po kategorii
def getsubcatlist(suvas):
    return_set = set()
    return_set.add(suvas)
    ixz = category.objects.filter(subcategory_of=suvas)
    for mnb in ixz:
        lak = category.objects.filter(subcategory_of=mnb)
        if lak.exists():
            return_set.add(mnb)
            for zum in lak:
                sam = getsubcatlist(zum)
                for mnx in sam:
                    return_set.add(mnx)
        else:
            return_set.add(mnb)
    return return_set
#eto dlya udaleniya der'ma iz korzini
def removeitemsfrombasket(mbf):
    user_id1 = get_object_or_404(User, pk=mbf)
    products_in_basket = trading_product_in_basket.objects.filter(user=user_id1).delete()

#главная++ (не рефактори)
def main(request):
    return render(request, 'automaximum/site_index.html')
#торговая_главная++(не рефактори)
def trading(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('trading_operation_product')
    else:
        return redirect('main')
#login++\logout++\(не рефактори)
def sign(request):
    action = request.GET.get('action', '')
    if action == 'logout':
        logout(request)
        return redirect('main')
    if action == 'login':
        print(request.user.is_authenticated)
        if request.user.is_authenticated == True:
            return redirect('main')
        else:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('trading')
            else:
                return render(request, 'automaximum/login.html',{
                })    
    return redirect('main')

#ajax(рефактори c jsom doma)
def trading_ajax(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.GET.get('subject') == 'productf':
            return_dict = dict()
            return_dict["items"] = list()
            #mashina
            if request.GET.get('type') == 'car' and request.GET.get('query')!= '':
                return_dict["type"]= request.GET.get('type')
                for mas in car.objects.filter(full_name__icontains=request.GET.get('query')):
                    product_dict = dict()
                    product_dict["id"] = mas.pk
                    product_dict["name"] = mas.full_name
                    return_dict["items"].append(product_dict)
            #dvigatel
            elif request.GET.get('type') == 'engine' and request.GET.get('query')!= '':
                return_dict["type"]= request.GET.get('type')
                for mas in engine.objects.filter(name__icontains=request.GET.get('query')):
                    product_dict = dict()
                    product_dict["id"] = mas.pk
                    product_dict["name"] = mas.name
                    return_dict["items"].append(product_dict)
            #analog
            elif request.GET.get('type') == 'analogue' and request.GET.get('query')!= '':
                return_dict["type"]= request.GET.get('type')
                ssam = category.objects.get(pk=request.GET.get('categoryid'))
                for mas in product.objects.filter(category=ssam).exclude(pk=request.GET.get('prodid')).filter(full_name__icontains=request.GET.get('query')):
                    product_dict = dict()
                    product_dict["id"] = mas.pk
                    product_dict["name"] = mas.full_name
                    return_dict["items"].append(product_dict)
            else:
                return None
            return_dict["len"] = int(len(return_dict["items"]))
            return JsonResponse(return_dict)
        elif request.GET.get('subject') == 'productlistbyname':
            return_dict = dict()
            return_dict["items"] = list()
            if request.GET.get('query')!= '':
                    for mas in product.objects.filter(full_name__icontains=request.GET.get('query')):
                        product_dict = dict()
                        product_dict["userid"] = request.user.pk
                        product_dict["id"] = mas.pk
                        product_dict["name"] = mas.full_name
                        return_dict["items"].append(product_dict)
            return_dict["len"] = int(len(return_dict["items"]))
            return JsonResponse(return_dict)
        elif request.GET.get('subject') == 'operation_product_list':
            return_dict = dict()
            return_dict["items"] = list()
            if request.GET.get('query')!= '':
                for mas in product.objects.filter(full_name__icontains=request.GET.get('query')):
                    product_dict = dict()
                    product_dict["id"] = mas.pk
                    product_dict["name"] = mas.full_name
                    return_dict["items"].append(product_dict)
            return_dict["len"] = int(len(return_dict["items"]))
            return JsonResponse(return_dict)
        elif request.GET.get('subject') == 'price_val':
            return_dict = dict()
            return_dict["items"] = list()
            if request.GET.get('query')!= '' and request.GET.get('price') != '':
                pri = price.objects.get(pk=request.GET.get('price'))
                pro = product.objects.get(pk=request.GET.get('query'))
                price_valq = price_value.objects.get(product=pro, price = pri)
                product_dict = dict()
                product_dict["name"] = price_valq.value
                return_dict["items"].append(product_dict)
            return_dict["len"] = int(len(return_dict["items"]))
            return JsonResponse(return_dict)
        elif request.GET.get('subject') == 'prices_val':
            if int(request.GET.get('count')) > 0:
                return_dict = dict()
                return_dict["items"] = list()
                pri = price.objects.get(pk=request.GET.get('price'))
                for zxcs in range(int(request.GET.get('count'))):
                    pro = product.objects.get(pk=request.GET.get('items['+str(zxcs)+']'))
                    price_valq = price_value.objects.get(product=pro, price = pri)
                    product_dict = dict()
                    product_dict["placing"] = str(zxcs)
                    product_dict["value"] = price_valq.value
                    return_dict["items"].append(product_dict)
                    price_valq, pro = None, None
                return_dict["len"] = int(len(return_dict["items"]))
                return JsonResponse(return_dict)
    else:
        return redirect('main')
#trading_tovari(korzina)++ add++\clear++\delete++(не рефактори)
def trading_addtobasket(request):
    if request.user.is_staff or request.user.is_superuser:    
        type = request.GET.get('type', '')
        product_id = request.GET.get('product_id', '')
        user_id = request.GET.get('user_id', '')
        amount = request.GET.get('amount', '')
        return_dict = dict()
        if type == 'add':
            user_id1 = get_object_or_404(User, pk=user_id)
            product_id1 = get_object_or_404(product, pk=product_id, deleted = False)
            new_product, created = trading_product_in_basket.objects.get_or_create(user=user_id1, product = product_id1)
            new_product.value += int(amount)
            new_product.save(force_update=True)
        if type == 'clear':
            user_id = request.GET.get('user_id', '')
            user_id1 = get_object_or_404(User, pk=user_id)
            if request.user == user_id1:
                products_in_basket = trading_product_in_basket.objects.filter(user=user_id1).delete()
        if type == 'delete':
            user_id1 = get_object_or_404(User, pk=user_id)
            product_id1 = get_object_or_404(product, pk=product_id)
            products_delete = trading_product_in_basket.objects.filter(user=user_id1, product = product_id1).delete()
        products_in_basket = trading_product_in_basket.objects.filter(user=user_id1)
        products_in_basket_count = products_in_basket.count()
        return_dict["products_in_basket_count"] = products_in_basket_count
        return_dict["products"] = list()
        for item in  products_in_basket:
            product_dict = dict()
            product_dict["userid"] = user_id1.pk
            product_dict["id"] = item.product.pk
            product_dict["name"] = item.product.full_name
            product_dict["value"] = item.value
            return_dict["products"].append(product_dict)
        return JsonResponse(return_dict)
    else:
        return redirect('main')

#additional(не рефактори)
def trading_additional(request):
    if request.user.is_superuser:
        return render(request, 'automaximum/trading_additional.html',{
        'nav_bar' : 'trading_additional',
        })
    #user ne admin
    else:
        return redirect('main')
#(не рефактори)
def trading_additional_option(request):
    if request.user.is_superuser:
        type = request.GET.get('type', '')
        class page:
            naming = None
            button_is = None
            button_bar = None
            obj_list = None
            texting = None
        #cennik
        if type == 'prices':
            page.button_is = True
            page.naming = 'Цены'
            if request.GET.get('object') == 'monitor_false':
                page.texting = "Отображаются объекты у которых не отслеживается цена"
                page.button_bar = 'monitor_false'
                page.obj_list = product.objects.filter(monitor_price=False)
            elif request.GET.get('object') == 'monitor':
                page.texting = "Отображаются объекты у которых цена не равна рекомендуемой"
                page.button_bar = 'monitor'
                page.obj_list = set()
                for i in price_value.objects.filter(monitor_price=True).order_by('product'):
                    if i.recomend_price != i.value:
                        page.obj_list.add(i)
        elif type == 'application':
            page.button_is = True
            page.naming = 'Остатки'
            if request.GET.get('object') == 'monitor_false':
                page.texting = "Отображаются объекты у которых не отслеживается остаток"
                page.button_bar = 'monitor_false'
                page.obj_list = product.objects.filter(monitor_amount=False)
            elif request.GET.get('object') == 'monitor':
                page.texting = "Отображаются объекты у которых итоговый остаток меньше минимального"
                page.button_bar = 'monitor'
                page.obj_list = set()
                for i in product.objects.filter(monitor_amount=True):
                    if i.amount0 < i.min_amount:
                        i.status = "this"
                        page.obj_list.add(i)
        elif type == 'amount_minus':
            page.texting = "Отображаются объекты с минусовым остатком"
            page.naming = 'Минусовой остаток'
            page.obj_list = product.objects.filter(amount0__lt=0)
        elif type == 'no_edited':
            page.texting = "Отображаются неотредактированные объекты"
            page.naming = 'Неотредактированные карты'
            page.obj_list = product.objects.filter(edited=False)
        elif type == 'need_to_edit':
            page.texting = "Отображаются карты товара помеченные на редактирование"
            page.naming = 'Карты товара на редактирование'
            page.obj_list = product.objects.filter(need_to_edit=True)
        elif type == 'need_to_edit_op':
            page.texting = "Отображаются товарные операции помеченные на редактирование"
            page.naming = 'Товарные операции на редактирование'
            page.obj_list = operation_product.objects.filter(need_to_edit=True)        
        else:
            return None
        return render(request, 'automaximum/trading_additional_option.html',{
        'nav_bar' : 'trading_additional',
        'page': page,
        'type' : type,
        })
    #user ne staff ili admin
    else:
        return redirect('main')
#не рефактори)
def trading_additional_prices(request):
    if request.user.is_superuser:
        qset = None
        if request.GET.get('operation_product') != None:
            qset= []
            wset= set()
            #lambda tormozit setami udobnee i bistree
            for i in operation_product_product_instance.objects.filter( operation_product=get_object_or_404( operation_product, pk= request.GET.get('operation_product'))):
                wset.add(i.product)
            for w in wset:
                ret_list = []
                ret_list.append(w)
                for k in price_value.objects.filter(product = w):
                    ret_list.append(k)
                qset.append(ret_list)
        #dlya drugih massovikh reaktirovaniy cen, k primeru po 分类，或者原厂或我不知道
        elif 'uslovie' == '':
            None
        else:            
            return redirect('trading')
        if request.method == "POST":
            for obj in qset:
                for i in obj[1:]:
                    print(i)
                    t = price_value.objects.get(pk=i.pk)
                    ###########cena
                    if request.POST[str(i.pk)+'-value'] == '':
                        t.value = None
                    else:
                        t.value = float(request.POST[str(i.pk)+'-value'])
                    ###########nacenka
                    if request.POST[str(i.pk)+'-nacenka'] == '':
                        t.nacenka = None
                    else:
                        t.nacenka = float(request.POST[str(i.pk)+'-nacenka'])
                    t.save(force_update=True)
            return redirect('/trading/operation_product/view?id=%s' % request.GET.get('operation_product'))
        return render(request, 'automaximum/trading_additional_prices.html',{
        'nav_bar' : 'trading_additional',
        'qset': qset,
        })
    #user ne staff ili admin
    else:
        return redirect('main')
#не рефактори)
def trading_additional_cars(request):
    if request.user.is_superuser:
        if request.GET.get('operation_product') != None:
            qset= None
            this_car = None
            if operation_product.objects.get(pk=request.GET.get('operation_product')).car != None:
                this_car = operation_product.objects.get(pk=request.GET.get('operation_product')).car
                qset= set()
                for i in operation_product_product_instance.objects.filter( operation_product=get_object_or_404( operation_product, pk= request.GET.get('operation_product'))):
                    qset.add(i.product)
        else:            
            return redirect('trading')
        if request.method == "POST" and this_car:
            for i in qset:
                p = product.objects.get(pk=i.pk)
                if request.POST.get(str(i.pk)+'-car', False) == 'on':
                    p.car.add(this_car)
                    p.save(force_update=True)
                else:
                    print('not got')
        return render(request, 'automaximum/trading_additional_cars.html',{
        'nav_bar' : 'trading_additional',
        'this_car':this_car,
        'qset': qset,
        })
    #user ne staff ili admin
    else:
        return redirect('main')

#settings++#не рефактори)
def trading_settings(request):
    if request.user.is_superuser:
        return render(request, 'automaximum/trading_settings.html',{
        'nav_bar' : 'trading_settings',
        })
    #user ne staff ili admin
    else:
        return redirect('main')
#view#не рефактори)
def trading_settings_view(request):
    if request.user.is_superuser:
        type = request.GET.get('type', '')
        object = request.GET.get('object', '')
        print(object=='')
        print(type)
        page_title = None
        obj_list = None
        button_is = None
        button_title = None
        if type == 'client':
            object = type
            page_title = "Управление Клиентами"
            button_is = True
            button_title = "Новый клиент"
            obj_list = client.objects.all().order_by('name')
        if type == 'cashbox':
            page_title = "Управление Кассовыми операциями"
            if object == 'cashbox':
                page_title = "Кассы"
                obj_list = cashbox.objects.all().order_by('name')
                button_is = True
                button_title = "Новая касса"
            if object == 'type_operation_money':
                page_title = "Виды кассовых операций"
                obj_list = type_operation_money.objects.all().order_by('name') 
                button_is = True
                button_title = "Новый вид кассовой операции"
        if type == 'product':
            page_title = 'Управление товарными операциями'
            if object == 'type_operation_product':
                page_title = "Виды товарных операций"            
                obj_list = type_operation_product.objects.all().order_by('name')
                button_is = True
                button_title = "Новый вид товарной операции"
            if object == 'storage':
                page_title = "Склады"            
                obj_list = storage.objects.all().order_by('name')
                button_is = True
                button_title = "Новый склад"
            if object == 'price':
                page_title = "Цены"            
                obj_list = price.objects.all().order_by('name')
                button_is = True
                button_title = "Новая цена"
        if type == 'user':
            page_title = "Управление пользователями"
            if object == 'user_profile':
                page_title = "Пользователи"            
                obj_list = user_profile.objects.all().order_by('name')
                button_is = True
                button_title = "Новый пользователь"
            if object == 'access_level':
                page_title = "Уровни доступа"            
                obj_list = access_level.objects.all().order_by('name')
                button_is = True
                button_title = "Новый уровень доступа"
        if type == 'product_list':
            page_title = "Управление товарами"
            if object == 'car':
                page_title = "Машины"            
                obj_list = car.objects.all().order_by('full_name')
                button_is = True
                button_title = "Новая машина"
            if object == 'engine':
                page_title = "Двигатели"            
                obj_list = engine.objects.all().order_by('name')
                button_is = True
                button_title = "Новый двигатель"
            if object == 'category':
                page_title = "Категории"            
                obj_list = category.objects.all().order_by('full_name')
                button_is = True
                button_title = "Новая категория"
            if object == 'manufacturer':
                page_title = "Производители"            
                obj_list = manufacturer.objects.all().order_by('name')
                button_is = True
                button_title = "Новый производитель"
            if object == 'part_of':
                page_title = "Расположения"            
                obj_list = part_of.objects.all().order_by('name')
                button_is = True
                button_title = "Новое Расположение"
            if object == 'characteristics':
                page_title = "Характеристики"            
                obj_list = characteristics.objects.all().order_by('name')
                button_is = True
                button_title = "Новая характеристика"
        return render(request, 'automaximum/trading_settings_view.html',{
        'nav_bar' : 'trading_settings',
        'type': type,
        'object': object,
        'obj_list': obj_list,
        'button_is':button_is,
        'page_title':page_title,
        'button_title':button_title,
        })
    #user ne staff ili admin    
    else:
        return redirect('main')
#manage(create \edit) - 
#client, cashbox, type_operation_money++, type_operation_product, storage, price, user, access_level
#car, engine, category, manufacturer, characteristics
     ##gospodi perepishi eto der'mo, eto 妈的笔啥都看不懂，以后要改修\gengxin的时候可以发现问题   
def trading_settings_manage(request):
    if request.user.is_superuser:
        type = request.GET.get('type', '')
        editformset= None
        object = request.GET.get('object', '')
        id = request.GET.get('id', '')
        if not object:
            return render(request, 'automaximum/site_index.html')
        #client
        if object == 'client':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = clientForm(request.POST)
                    if form.is_valid():
                        client = form.save(commit=False)
                        client.creator = created_by
                        client.save()
                        return redirect('/trading/settings/manage?type=edit&object=%s&id=%s' % (object, client.pk))
                else:
                    form = clientForm()
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'client',
                        'page_type' : 'create',
                        'page_name' : "Клиент",
                    })  
            if type == 'edit':
                client1 = client_mm.get(pk=id)
                if request.method == "POST":
                    created_by = request.user
                    form = clientForm(request.POST, instance=client1)
                    if form.is_valid():
                        client1 = form.save(commit=False)
                        client1.save()
                        return redirect('/trading/settings/view?type=%s' % object )
                else:
                    page_name = "Клиент"
                    form = clientForm(instance=client1)
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'cashbox1': client1,
                        'form': form,
                        'object1': client1, 
                        'page' : 'client',
                        'page_type' : 'edit',
                        'page_name' : page_name,
                    })
        #cashbox        
        if object == 'cashbox':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = cashboxForm(request.POST)
                    if form.is_valid():
                        cashbox = form.save(commit=False)
                        cashbox.save()
                        return redirect('trading_settings')
                else:
                    form = cashboxForm()
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'cashbox',
                        'page_type' : 'create',
                        'page_name' : "Касса",
                    })
            if type == 'edit':
                cashbox1 = cashbox_mm.get(pk=id)
                if request.method == "POST":
                    created_by = request.user
                    form = cashboxForm(request.POST, instance=cashbox1)
                    if form.is_valid():
                        cashbox1 = form.save(commit=False)
                        cashbox1.save()
                        return redirect('trading_settings')
                else:
                    form = cashboxForm(instance=cashbox1)
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'cashbox1': cashbox1,
                        'form': form,
                        'object1': cashbox1, 
                        'page' : 'type_operation_money',
                        'page_type' : 'edit',
                        'page_name' : "Касса",
                    })
        #type_operation_money        
        if object == 'type_operation_money':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = type_operation_moneyForm(request.POST)
                    if form.is_valid():
                        type_operation_money = form.save(commit=False)
                        type_operation_money.save()
                        return redirect('trading_settings')
                else:
                    form = type_operation_moneyForm()
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'type_operation_money',
                        'page_type' : 'create',
                        'page_name' : "Кассовая операция",
                    })
            if type == 'edit':
                type_operation_money1 = type_operation_money_mm.get(pk=id)
                if request.method == "POST":
                    created_by = request.user
                    form = type_operation_moneyForm(request.POST, instance=type_operation_money1)
                    if form.is_valid():
                        type_operation_money1 = form.save(commit=False)
                        type_operation_money1.save()
                        return redirect('trading_settings')
                else:
                    form = type_operation_moneyForm(instance=type_operation_money1)
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'type_operation_money1': type_operation_money1,
                        'form': form,
                        'object1': type_operation_money1, 
                        'page' : 'type_operation_money',
                        'page_type' : 'edit',
                        'page_name' : "Кассовая операция",
                    })
        #type_operation_product
        if object == 'type_operation_product':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = type_operation_productForm(request.POST)
                    if form.is_valid():
                        type_operation_product = form.save(commit=False)
                        type_operation_product.save()
                        return redirect('trading_settings')
                else:
                    form = type_operation_productForm()
                    del form.fields["default_price"]
                    del form.fields["default_client"]
                    del form.fields["creates"]
                    del form.fields["changes_price"]
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'type_operation_product',
                        'page_type' : 'create',
                        'page_name' : "Товарная операция",
                    })
            if type == 'edit':
                type_operation_product1 = type_operation_product_mm.get(pk=id)
                if request.method == "POST":
                    created_by = request.user
                    form = type_operation_productForm(request.POST, instance=type_operation_product1)
                    del form.fields["type"]
                    if form.is_valid():
                        type_operation_product1 = form.save(commit=False)
                        type_operation_product1.save()
                        return redirect('trading_settings')
                else:
                    form = type_operation_productForm(instance=type_operation_product1)
                    form.fields["creates"].empty_label=None
                    if type_operation_product1.type == "plus":
                        form.fields["creates"].queryset = type_operation_money_mm.filter(type='minus')
                    if type_operation_product1.type == "minus":
                        form.fields["creates"].queryset = type_operation_money_mm.filter(type='plus')
                    del form.fields["type"]
                    if type_operation_product1.type == "minus":
                        del form.fields["changes_price"]
                    if type_operation_product1.type == "plus":
                        del form.fields["default_price"]
                        del form.fields["default_client"]
                    if type_operation_product1.type == "minusplus":
                        del form.fields["default_price"]
                        del form.fields["default_client"]
                        del form.fields["creates"]
                        del form.fields["changes_price"]
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'type_operation_product1': type_operation_product1,
                        'form': form,
                        'object1': type_operation_product1, 
                        'page' : 'type_operation_product',
                        'page_type' : 'edit',
                        'page_name' : "Товарная операция",
                    })
        #storage
        if object == 'storage':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = storageForm(request.POST)
                    if form.is_valid():
                        storage = form.save(commit=False)
                        for product in product_mm:
                            amount_on_storage.objects.create(storage=storage, product=product)
                        storage.save()
                        return redirect('trading_settings')
                else:
                    form = storageForm()
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'storage',
                        'page_type' : 'create',
                        'page_name' : "Склад",
                    })
            if type == 'edit':
                storage1 = storage_mm.get(pk=id)
                if request.method == "POST":
                    created_by = request.user
                    form = storageForm(request.POST, instance=storage1)
                    if form.is_valid():
                        storage1 = form.save(commit=False)
                        storage1.save()
                        return redirect('trading_settings')
                else:
                    form = storageForm(instance=storage1)
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'storage1': storage1,
                        'form': form,
                        'object1': storage1, 
                        'page' : 'storage',
                        'page_type' : 'edit',
                        'page_name' : "Склад",
                    })
        #price
        if object == 'price':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = priceForm(request.POST)
                    if form.is_valid():
                        price = form.save(commit=False)
                        for product in product_mm:
                            price_value.objects.create(price=price, product=product, value=0, recomend_price=0)                
                        price.save()
                        return redirect('trading_settings')
                else:
                    form = priceForm()
                    form.fields["analogue"].empty_label='Закупочная'
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'price',
                        'page_type' : 'create',
                        'page_name' : "Цена",
                    })
            if type == 'edit':
                price1 = price_mm.get(pk=id)
                if request.method == "POST":
                    created_by = request.user
                    form = priceForm(request.POST, instance=price1)
                    if form.is_valid():
                        price1 = form.save(commit=False)
                        price1.save()
                        return redirect('trading_settings')
                else:
                    form = priceForm(instance=price1)
                    form.fields["analogue"].empty_label='Закупочная'
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'price1': price1,
                        'form': form,
                        'object1': price1, 
                        'page' : 'price',
                        'page_type' : 'edit',
                        'page_name' : "Цена",
                    })
        #user nedodelano
        if object == 'user_profile':
            if type == 'create':
                if request.method == 'POST':
                    created_by = request.user
                    user_form = userForm(data=request.POST)
                    profile_form = user_profileForm(data=request.POST)
                    if user_form.is_valid() and profile_form.is_valid():
                        user = user_form.save()
                        user.set_password(user.password)
                        user.is_staff = True
                        user.save()
                        profile = profile_form.save(commit=False)
                        profile.user = user
                        profile.save()
                        return redirect('trading_settings')
                    else:
                        print (userForm.errors, user_profileForm.errors)
                else:
                    user_form = userForm()
                    profile_form = user_profileForm()
                    return render(request, 'automaximum/trading_settings_manage.html',{
                    'nav_bar' : 'trading_settings',
                    'page' : 'user',
                    'page_type' : 'create',                    
                    'user_form': user_form,
                    'profile_form': profile_form, 
                    'page_name' : "Пользователь",
                    })                  
        #access_level
        if object == 'access_level':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = access_levelForm(request.POST)
                    if form.is_valid():
                        access_level = form.save(commit=False)
                        access_level.save()
                        return redirect('trading_settings')
                else:
                    form = access_levelForm()
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'access_level',
                        'page_type' : 'create',
                        'page_name' : "Уровень доступа",
                    })
            if type == 'edit':
                access_level1 = access_level_mm.get(pk=id)
                if request.method == "POST":
                    created_by = request.user
                    form = access_levelForm(request.POST, instance=access_level1)
                    if form.is_valid():
                        access_level1 = form.save(commit=False)
                        access_level1.save()
                        return redirect('trading_settings')
                else:
                    form = access_levelForm(instance=access_level1)
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'access_level1': access_level1,
                        'form': form,
                        'object1': access_level1, 
                        'page' : 'access_level',
                        'page_type' : 'edit',
                        'page_name' : "Уровень доступа",
                    })
        #car
        if object == 'car':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = carForm(request.POST)
                    if form.is_valid():
                        car = form.save()
                        car.save()
                        return redirect('trading_settings')
                else:
                    form = carForm()
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'car',
                        'page_type' : 'create',
                        'page_name' : "Машина",
                    })  
            if type == 'edit':
                car1 = car_mm.get(pk=id)
                if request.method == "POST":
                    created_by = request.user
                    form = carForm(request.POST, instance=car1)
                    if form.is_valid():
                        car1 = form.save()
                        car1.save()
                        return redirect('trading_settings')
                else:
                    form = carForm(instance=car1)
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'car1': car1,
                        'form': form,
                        'object1': car1, 
                        'page' : 'car',
                        'page_type' : 'edit',
                        'page_name' : "Машина",
                    })
        #engine
        if object == 'engine':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = engineForm(request.POST)
                    if form.is_valid():
                        engine = form.save(commit=False)
                        engine.save()
                        return redirect('trading_settings')
                else:
                    form = engineForm()
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'engine',
                        'page_type' : 'create',
                        'page_name' : "Двигатель",
                    })  
            if type == 'edit':
                engine1 = engine_mm.get(pk=id)
                if request.method == "POST":
                    created_by = request.user
                    form = engineForm(request.POST, instance=engine1)
                    if form.is_valid():
                        engine1 = form.save(commit=False)
                        engine1.save()
                        return redirect('trading_settings')
                else:
                    form = engineForm(instance=engine1)
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'engine1': engine1,
                        'form': form,
                        'object1': engine1, 
                        'page' : 'engine',
                        'page_type' : 'edit',
                        'page_name' : "Двигатель",
                    })
        #category
        if object == 'category':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = categoryForm(request.POST)
                    if form.is_valid():
                        category = form.save()
                        category.save()
                        return redirect('trading_settings')
                else:
                    form = categoryForm()
                    del form.fields["characteristics_forname"]
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'category',
                        'page_type' : 'create',
                        'page_name' : "Категория",
                    })
            if type == 'edit':
                category1 = category_mm.get(pk=id)
                category1_backup_name = category1.name
                if request.method == "POST":
                    created_by = request.user
                    cs1 = set()
                    backup_category_characteristics = category1.characteristics.all()
                    for kizx in backup_category_characteristics:
                        cs1.add(kizx)
                    form = categoryForm(request.POST, instance=category1)
                    if form.is_valid():
                        category2 = form.save()
                        #eto na udaleniye
                        doa = category2.characteristics.all()
                        cs2 = set()
                        for kixc in doa:
                            cs2.add(kixc)
                        if cs1 != cs2:
                            products_asd_list = product_mm.filter(category=category1)
                            hzcheto = cs1 - cs2
                            for sadf in hzcheto:
                                for asd in products_asd_list:
                                    qwer = characteristics_value.objects.filter(characteristics=sadf, product=asd)
                                    for lzx in qwer:
                                        #qwer.delete()
                                        lzx.delete()
                            #eto na dobavleniye
                            dobavit = cs2 - cs1
                            for kmz in dobavit:
                                for zasd in products_asd_list:
                                    characteristics_value.objects.create(product=zasd, characteristics= kmz)
                        if category1_backup_name != category2.name and category2.useinfullname is True:
                            for asde in product_mm.filter(category = category2):
                                asde.save()
                        category2.save()
                        return redirect('trading_settings')
                else:
                    form = categoryForm(instance=category1)
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'category1': category1,
                        'form': form,
                        'object1': category1, 
                        'page' : 'category',
                        'page_type' : 'edit',
                        'page_name' : "Категория",
                    })
        #manufacturer
        if object == 'manufacturer':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = manufacturerForm(request.POST)
                    if form.is_valid():
                        manufacturer = form.save(commit=False)
                        manufacturer.save()
                        return redirect('trading_settings')
                else:
                    form = manufacturerForm()
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'manufacturer',
                        'page_type' : 'create',
                        'page_name' : "Производитель",
                    })  
            if type == 'edit':
                manufacturer1 = manufacturer_mm.get(pk=id)
                manufacturer1_backup_name = manufacturer1.name
                if request.method == "POST":
                    created_by = request.user
                    form = manufacturerForm(request.POST, instance=manufacturer1)
                    if form.is_valid():
                        manufacturer1 = form.save(commit=False)
                        if manufacturer1_backup_name != manufacturer1.name:
                            for kkk in product_mm.filter(manufacturer=manufacturer1):
                                kkk.save()
                        manufacturer1.save()
                        return redirect('trading_settings')
                else:
                    form = manufacturerForm(instance=manufacturer1)
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'manufacturer1': manufacturer1,
                        'form': form,
                        'object1': manufacturer1, 
                        'page' : 'manufacturer',
                        'page_type' : 'edit',
                        'page_name' : "Производитель",
                    })
        #Расположение
        if object == 'part_of':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = part_ofForm(request.POST)
                    if form.is_valid():
                        part_of = form.save(commit=False)
                        part_of.save()
                        return redirect('trading_settings')
                else:
                    form = part_ofForm()
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'part_of',
                        'page_type' : 'create',
                        'page_name' : "Расположение",
                    })  
            if type == 'edit': 
                part_of1 = part_of_mm.get(pk=id)
                if request.method == "POST":
                    created_by = request.user
                    form = part_ofForm(request.POST, instance=part_of1)
                    if form.is_valid():
                        part_of1 = form.save(commit=False)
                        part_of1.save()
                        return redirect('trading_settings')
                else:
                    form = part_ofForm(instance=part_of1)
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'part_of1': part_of1,
                        'form': form,
                        'object1': part_of1, 
                        'page' : 'part_of',
                        'page_type' : 'edit',
                        'page_name' : "Расположение",
                    })
        #characteristics
        if object == 'characteristics':
            if type == 'create':
                if request.method == "POST":
                    created_by = request.user
                    form = characteristicsForm(request.POST)
                    if form.is_valid():
                        characteristics = form.save(commit=False)
                        characteristics.save()
                        return redirect('trading_settings')
                else:
                    form = characteristicsForm()
                    del form.fields["edinica"]
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'form': form,
                        'page' : 'characteristics',
                        'page_type' : 'create',
                        'page_name' : "Характеристика",
                    })  
            if type == 'edit':
                characteristics1 = characteristics_mm.get(pk=id)
                if characteristics1.type == 'choice':
                    editformset1 = modelformset_factory(characteristics_choices, form=characteristics_choicesForm, extra = 1)  
                if request.method == "POST":
                    created_by = request.user
                    form = characteristicsForm(request.POST, instance=characteristics1)
                    del form.fields["type"]
                    if characteristics1.type == 'choice':
                        editformset = editformset1(request.POST, queryset=characteristics_choices.objects.filter(characteristics=characteristics1))
                    if characteristics1.type == 'choice':
                        if form.is_valid() and editformset.is_valid():
                            characteristics1 = form.save(commit=False)
                            for kzx in editformset:
                                ming = kzx.save(commit=False)
                                ming.characteristics = characteristics1
                                ming.save()
                                if ming.text == '':
                                    ming.delete()
                            characteristics1.save()
                            return redirect('trading_settings')
                    else:
                        if form.is_valid():
                            print('doshlo')
                            characteristics1 = form.save(commit=False)
                            characteristics1.save()
                            return redirect('trading_settings')
                else:
                    form = characteristicsForm(instance=characteristics1)
                    del form.fields["type"]
                    if characteristics1.type != 'int':
                        del form.fields["edinica"]
                    if characteristics1.type == 'choice':
                        editformset = editformset1(queryset=characteristics_choices.objects.filter(characteristics=characteristics1))
                        for ksaq in editformset:
                            ksaq.fields["text"].label = ''
                    return render(request, 'automaximum/trading_settings_manage.html',{
                        'nav_bar' : 'trading_settings',
                        'characteristics1': characteristics1,
                        'form': form,
                        'object1': characteristics1, 
                        'page' : 'characteristics',
                        'page_type' : 'edit',
                        'page_name' : "Характеристика",
                        'editformset': editformset,
                    })

    #user ne staff ili admin              
    else:
        return redirect('main')


#картотека обычная##############
def trading_products_list(request):
    if request.user.is_staff or request.user.is_superuser:
        view_type = request.GET.get('view_type', '')
        #картотека(аргус)
        if view_type == "argus":
            storage_list = storage.objects.all().order_by('pk')
            price_list = price.objects.all().order_by('pk')
            state = request.GET.get('state', '')
            search_type = request.GET.get('search_type', '')
            search_product = request.GET.get('search_product', '')
            if search_type == "article":
                products_list = product.objects.filter(argus_article__icontains=search_product).distinct().order_by('argus_article')
            else:
                search_type = "name"
                products_list = product.objects.filter(argus_name__icontains=search_product).distinct().order_by('argus_article')
            if state == "left":
                products_list = product.objects.filter(amount0__gt=0)
            return render(request, 'automaximum/trading_products_list_argus.html', {
            'nav_bar' : 'trading_products_list',
            'button_bar' : 'trading_products_list_argus',
            'products_list': products_list,
            'search_product': search_product,
            'storage_list': storage_list,
            'price_list': price_list,
            'search_type': search_type,
            'state': state,
            })    
        
        else:
            #обычная            
            type = request.GET.get('type', 'name')
            item = request.GET.get('search_product', '')
            items_product = product.objects.none()
            #car
            car_all = car.objects.filter(subcategory_of=None)
            car_subcatlist = None
            currcar = None
            car_products_list= None
            smset2 = None
            #engine
            engine_all = engine.objects.all()
            engine_list = None
            engin = None
            #cat
            cat_all = category.objects.filter(subcategory_of=None).order_by('full_name')
            curr_cat = None
            cat_list = None
            categor = None
            subcat_list = None
            #char
            char_cat_all = category.objects.all().order_by('full_name')
            charsel = None
            quests = None
            characteristicszz = None
            dlyaproverkichar = None
            #manuf
            manufact_all = manufacturer.objects.all()
            manufact_list = None
            manuf = None
            #by bname
            if type == "name":
                if item is not '':
                    items_product = product.objects.filter(Q(full_name__icontains=item) | Q(article_alt__icontains=item))
            #sdelai
            if type == "car":
                if item is not '':
                    yui = car.objects.filter(full_name=item)
                    if not yui.exists():
                        yui = car.objects.filter(full_num=item)
                        if not yui.exists():
                            yui = car.objects.filter(full_name__icontains=item).distinct()
                    if yui.count() == 1:
                        car_set = set()
                        car_products_list = set()
                        ########################
                        #eto daet spisok vseh productov s part of
                        car_partofcar_list = set()
                        #eto spisok vseh mestopolojeniy
                        smset = set()
                        ####################
                        for z in yui:
                            car_all = car.objects.filter(subcategory_of = z)
                            currcar = z
                            car_set.add(currcar)
                            olos = currcar.subcategory_of
                            while olos is not None:
                                car_set.add(olos)
                                olos = olos.subcategory_of
                        for ims in car_set:
                            #poisk predmetov po mashine
                            kic = part_of_car.objects.filter(car = ims)
                            for zvc in kic:
                                if zvc.part_of.exists():
                                    car_partofcar_list.add(zvc)
                            ozx = product.objects.filter(car=ims)
                            for imz in ozx:
                                car_products_list.add(imz)
                            asd = ims.engine.all()
                            for dsa in asd:
                                #poisk predmetov po dvigatelyu
                                zlx = part_of_car.objects.filter(engine=dsa)
                                for dns in zlx:
                                    if dns.part_of.exists():
                                        car_partofcar_list.add(dns)
                                zyn = product.objects.filter(engine=dsa)
                                for dey in zyn:
                                    car_products_list.add(dey)
                        #kostili pzdc
                        for htr in car_partofcar_list:
                            for dei in htr.part_of.all():
                                smset.add(dei)
                        smset2 = []
                        #sozdaem list
                        for kmns in smset:
                            addlist = []
                            addlist.append(kmns)
                            for jer in car_partofcar_list:
                                for kuw in jer.part_of.all():
                                    if kuw == kmns:
                                        addlist.append(jer)
                            smset2.append(addlist)
                        for ore in smset2:
                            print('smset')
                            print(ore)
                    else:
                        car_all = yui
                    #cars_list = car.objects.filter(subcategory_of=zza)
                    #productsin_list = product.objects.filter(car = )
            #engine++
            if type == "engine":
                if item is not '':
                    engine_all = None
                    engin = engine.objects.filter(name__icontains=item)
                    if engin.count() == 1:
                        for z in engin:
                            engin = engin.get(name = z.name)
                            engine_list = product.objects.filter(engine=engin)
                    else:
                        engine_all = engin
            #category++
            if type == "category":
                if item is not '':
                    cat_all = None
                    categor = category.objects.filter(name__icontains=item)
                    if categor.count() == 1:
                        for z in categor:    
                            cat_listfor = set()
                            cat_list = set()                    
                            categor = categor.get(name = z.name)
                            curr_cat = product.objects.filter(category=categor)
                            subcat_list = category.objects.filter(subcategory_of=z)
                            for zozh in subcat_list:
                                klzx = getsubcatlist(zozh)
                                for kdsa in klzx:
                                    cat_listfor.add(kdsa)
                            for kzx in cat_listfor:
                                mxc = product.objects.filter(category=kzx)
                                for jds in mxc:
                                    cat_list.add(jds)
                    else:
                        cat_all = categor
            #sdelai
            if type == "chars":
                if item is not '':
                    characteristicszz = set()
                    cs1 = set()
                    cs2 = set()
                    quests = get_object_or_404(category, name=item)
                    char_cat_all = None
                    charsel = quests.characteristics.all()
                    chetotam = 0
                    for cxz in charsel:
                        if request.GET.get(str(cxz.name)) != None  and request.GET.get(str(cxz.name)) != '':    
                            sim = request.GET.get(str(cxz.name))
                            chetotam = chetotam + 1
                            if sim != '':
                                dlyaproverkichar = 'smth'
                            if cxz.type == "int":
                                #tut query s razbrosom
                                lkm = characteristics_value.objects.filter(characteristics=cxz, value = float(sim))
                            if cxz.type == "string":
                                lkm = characteristics_value.objects.filter(characteristics=cxz, text = sim)
                            if cxz.type == "choice":
                                lkm = characteristics_value.objects.filter(characteristics=cxz, choice = sim)
                            for miz in lkm:
                                if miz.product.category == quests:                                    
                                    characteristicszz.add(miz)
                    print(chetotam)
                    for smths in characteristicszz:
                        cs1.add(smths)
                        for smths1 in characteristicszz:
                            if smths.product == smths1.product:
                                cs1.add(smths1)
                        print(cs1)
                        if len(cs1) == chetotam:
                            print('eto ono')
                            for zub in cs1:
                                cs2.add(zub.product)
                        cs1 = set()
                    characteristicszz = cs2
            #mmanf
            if type == "manufact":
                if item is not '':
                    manufact_all = None
                    manuf = manufacturer.objects.filter(name__icontains=item)
                    if manuf.count() == 1:
                        for z in manuf:
                            manuf = manuf.get(name = z.name)
                            manufact_list = product.objects.filter(manufacturer=manuf)
                    else:
                        manufact_all = manuf

            return render(request, 'automaximum/trading_products_list.html', {
                'button_bar' : 'trading_products_list',
                'nav_bar' : 'trading_products_list',
                'items_product': items_product,
                #car
                'car_all': car_all,
                'car_subcatlist':car_subcatlist,
                'currcar':currcar,
                'car_products_list':car_products_list,
                'smset2': smset2,
                #engine
                'engine_all': engine_all,
                'engin': engin,
                'engine_list': engine_list,
                #category
                'cat_all': cat_all,
                'cat_list': cat_list,
                'curr_cat': curr_cat,
                'subcat_list': subcat_list,
                'categor': categor,
                #char
                'char_cat_all': char_cat_all,
                'quests':quests,
                'charsel': charsel,
                'characteristicszz': characteristicszz,
                'dlyaproverkichar': dlyaproverkichar,
                #manufacturer
                'manufact_all': manufact_all,
                'manuf': manuf,
                'manufact_list': manufact_list,
                'item': item,
                'type': type,
                })
        
        #else:
            #return render(request, 'automaximum/trading_products_list.html', {
            #'nav_bar' : 'trading_products_list',
            #'type': "name",
            #'button_bar' : 'trading_products_list',
            #})
    else:
        return redirect('main')
#view
def trading_products_view(request):
    if request.user.is_staff or request.user.is_superuser:
        object = request.GET.get('object', '')
        id = request.GET.get('id', '')
        #product
        if object == "product":
            view_product = get_object_or_404(product, pk=id)
            product_characteristics = characteristics_value.objects.filter(product = view_product) 
            product_amount = amount_on_storage.objects.filter(product = view_product)
            product_shou = set()
            zub = type_operation_product.objects.filter(type = 'plus')
            for kls in zub:
                zzu = operation_product.objects.filter(type = kls, approved = True)
                for olk in zzu:
                    iks = operation_product_product_instance.objects.filter(operation_product = olk, product = view_product)
                    for mny in iks:
                        product_shou.add(mny)
            product_fa = set()
            rys = type_operation_product.objects.filter(type = 'minus')
            for kls in rys:
                zzu = operation_product.objects.filter(type = kls, approved = True)
                for olk in zzu:
                    iks = operation_product_product_instance.objects.filter(operation_product = olk, product = view_product)
                    for mny in iks:
                        product_fa.add(mny)
            kuss = type_operation_product.objects.filter(type = 'minusplus')
            for dei in kuss:
                zzu = operation_product.objects.filter(type = dei, approved = True)
                for olk in zzu:
                    iks = operation_product_product_instance.objects.filter(operation_product = olk, product = view_product)
                    for mny in iks:
                        product_fa.add(mny)
                        product_shou.add(mny)
            analogi = set()
            naproverku = set()
            analogi.add(view_product)
            dei = analogi - naproverku
            while len(dei) != 0:
                dei = analogi - naproverku
                for bmj in dei:
                    naproverku.add(bmj)
                    dei = analogi - naproverku
                    izk = bmj.analogue.all()
                    for som in izk:
                        analogi.add(som)
            analogi.remove(view_product)
            prices = price_value.objects.filter(product = view_product)
            avto = view_product.car.all()
            dvigatel = view_product.engine.all()
            return render(request, 'automaximum/trading_products_view.html', {
            'nav_bar' : 'trading_products_list',
            'view_product': view_product,
            'product_characteristics': product_characteristics,
            'product_amount': product_amount,
            'product_shou': product_shou,
            'product_fa': product_fa,
            'analogi': analogi,
            'prices': prices,
            'avto': avto,
            'dvigatel': dvigatel,
            })
    else:
        return redirect('main')
#новая карта товара
def trading_products_create(request):
    if request.user.is_staff or request.user.is_superuser:
        create = request.GET.get('create', '')
        #product
        if create == "product":
            if request.method == "POST":
                form = productForm(request.POST)
                if not request.user.is_superuser:
                    del form.fields["price0"]
                if form.is_valid():
                    obje = form.save()
                    memory_action.objects.create(name = 'Новая карта товара', action = 'Создание новой карты' + str(obje) + ' ' , created_date = timezone.now())
                    obje.save()
                    for i in storage.objects.all():
                        amount_on_storage.objects.create(storage=i, product=obje, amount = 0)
                    for i in price_mm:
                        price_value.objects.create(price=i, product=obje, value = 0,recomend_price = 0, monitor_price=obje.monitor_price)
                    for i in obje.category.characteristics.all():
                        characteristics_value.objects.create(characteristics=i, product=obje)
                    for i in obje.car.all():
                        part_of_car.objects.create(product=obje, car=i)
                    for i in obje.engine.all():
                        part_of_car.objects.create(product=obje, engine=i)
                    return redirect('/trading/products/edit?id=%s' %obje.pk)
            else:
                form = productForm()
                form.fields["category"].empty_label=None
                #krasotisha!
                del form.fields["car"]
                del form.fields["analogue"]
                del form.fields["engine"]
                if not request.user.is_superuser:
                    del form.fields["price0"]
            return render(request, 'automaximum/trading_products_create.html', {
            'nav_bar' : 'trading_products_list',
            'form': form,
            'page' : 'new',
            'page_name' : "Продукция"
            })
    #if no
        else:
            return render(request, 'automaximum/trading_index.html')
    else:
        return redirect('main')
#product edit
def trading_products_edit(request):
    if request.user.is_staff or request.user.is_superuser:
        id = request.GET.get('id', '')
        product1 = get_object_or_404(product, pk=id)
        product_characteristics = characteristics_value.objects.filter(product=product1)
        editformset1 = modelformset_factory(characteristics_value, form=characteristics_valueForm, extra=0)
        editformset2 = modelformset_factory(price_value, form=price_valueForm, extra=0)
        editformset3 = modelformset_factory(part_of_car, form=part_of_carForm, extra=0)
        product_backup_category = product1.category
        if request.method == "POST":
            if request.POST.get('deleteit', '') == 'true' and product1.deletefree == True:
                product1.delete()
            form = productForm(request.POST, instance=product1)
            cs1= set()
            for kvc in product1.car.all():
                cs1.add(kvc)
            cs3 = set()
            for kvh in product1.engine.all():
                cs3.add(kvh)
            editformset = editformset1(request.POST, queryset=characteristics_value.objects.filter(product=product1))
            priceformset = editformset2(request.POST, queryset=price_value.objects.filter(product=product1), prefix='price')
            part_of_carformset = editformset3(request.POST, queryset=part_of_car.objects.filter(product=product1), prefix = 'partofcar')
            if not request.user.is_superuser:
                del form.fields["price0"]
            if form.is_valid() and editformset.is_valid() and priceformset.is_valid() and part_of_carformset.is_valid():
                product1 = form.save()
                #chasti avtomobilya
                part_of_carformset.save()
                cs2=set()
                for zxa in product1.car.all():
                    cs2.add(zxa)
                if cs1 != cs2:
                    #na udaleniye
                    hzcheto = cs1 - cs2
                    for ams in hzcheto:
                        part_of_car.objects.filter(car=ams, product=product1).delete()
                    #na dobavleniye
                    dobavit = cs2 - cs1
                    for kmz in dobavit:                            
                        part_of_car.objects.create(product=product1, car=kmz)
                cs4 = set()
                for nhd in product1.engine.all():
                    cs4.add(nhd)                
                if cs3 != cs4:
                    #na udaleniye
                    hzcheto = cs3 - cs4
                    for ams in hzcheto:
                        part_of_car.objects.filter(engine=ams, product=product1).delete()
                    #na dobavleniye
                    dobavit = cs4 - cs3
                    for kmz in dobavit:                            
                        part_of_car.objects.create(product=product1, engine=kmz)
                #harakteristiki
                editformset.save()
                if product_backup_category != product1.category:
                    characteristics_value.objects.filter(product=product1).delete()
                    for i in product1.category.characteristics.all():
                        if i.type=='int':
                            characteristics_value.objects.create(characteristics=i, product=product1)
                        elif i.type=='string':
                            characteristics_value.objects.create(characteristics=i, product=product1)
                        elif i.type=='choice':
                            characteristics_value.objects.create(characteristics=i, product=product1)
                #ceni
                for i in priceformset:
                    z = i.save(commit=False)
                    if z.value == None:
                        z.value = 0
                    z.save()
                product1.edited=True
                product1.save()
                #arhiv
                #edit
                return redirect('/trading/products/view?object=product&id=%s' % product1.pk)
        else:
            form = productForm(instance=product1)
            form.fields["category"].empty_label=None
            editformset = editformset1(queryset=characteristics_value.objects.filter(product=product1))
            for kkl in editformset:
                if kkl.instance.characteristics.type == 'int':
                    kkl.fields["value"].label = str(kkl.instance.characteristics)
                    kkl.fields["value"].widget.attrs.update({'class': 'form-control'})
                    del kkl.fields["text"]
                    del kkl.fields["choice"]
                if kkl.instance.characteristics.type == 'choice':
                    kkl.fields["choice"].label = str(kkl.instance.characteristics)
                    kkl.fields["choice"].widget.attrs.update({'class': 'form-control'})
                    del kkl.fields["text"]
                    del kkl.fields["value"]                
                if kkl.instance.characteristics.type == 'string':
                    kkl.fields["text"].label = str(kkl.instance.characteristics)
                    kkl.fields["text"].widget.attrs.update({'class': 'form-control'})
                    del kkl.fields["value"]
                    del kkl.fields["choice"]
                
            priceformset = editformset2(queryset=price_value.objects.filter(product=product1), prefix='price')
            for kkl in priceformset:
                fields = list(kkl)
                kkl.part1, kkl.part2,kkl.part3 = fields[0], fields[1],fields[2:]
                fields= None
                kkl.fields["value"].label = str(kkl.instance.price)
                kkl.fields["nacenka"].label = ('Наценка на цену '+ str(kkl.instance.price))
                kkl.fields["value"].widget.attrs.update({'class': 'form-control'})
                kkl.fields["nacenka"].widget.attrs.update({'class': 'form-control'})
            part_of_carformset = editformset3(queryset=part_of_car.objects.filter(product=product1).order_by('engine').order_by('car'), prefix = 'partofcar')
            for kls in part_of_carformset:
                kls.fields["part_of"].widget.attrs.update({'class': 'form-control'})
                if kls.instance.car != None:
                    kls.fields["part_of"].label = str(kls.instance.car)
                else:
                    kls.fields["part_of"].label = str(kls.instance.engine)
            #for characteristics in product_characteristics:
                #edit_form = characteristics_valueForm(instance = product_characteristics)
            #krasotisha!
            del form.fields["car"]
            del form.fields["analogue"]
            del form.fields["engine"]
            if not request.user.is_superuser:
                del form.fields["price0"]

        return render(request, 'automaximum/trading_products_create.html', {
        'nav_bar' : 'trading_products_list',
        'form': form,
        'product_characteristics': product_characteristics,
        'editformset': editformset,
        'priceformset': priceformset,
        'part_of_carformset': part_of_carformset,
        'product1': product1,
        'page' : 'edit',
        })
    else:
        return redirect('main')          


#кассовые операции++
def trading_operation_cashbox(request):
    if request.user.is_staff or request.user.is_superuser:
        cashbox_all = None
        if request.user.is_superuser is True:
            cashbox_all = cashbox.objects.all().order_by('name')
        else:
            cashbox_all = cashbox.objects.all().filter(admin_cashbox=False).order_by('name')
        query_cashbox = request.GET.get('cashbox', '')
        if query_cashbox == "":
            cashbox1 = cashbox_all.all()[0]
        else:
            if request.user.is_superuser:
                cashbox1 = get_object_or_404(cashbox, pk=query_cashbox)
            else:
                cashbox1 = get_object_or_404(cashbox, pk=query_cashbox, admin_cashbox=False)
        operation_money1 = operation_money.objects.filter(Q(cashbox=cashbox1) | Q(cashbox_recieve=cashbox1)).order_by('-created_date')
        return render(request, 'automaximum/trading_operation_cashbox.html', {
        'nav_bar' : 'trading_operation_cashbox',
        'cashbox_all': cashbox_all,
        'cashbox1': cashbox1,
        'operation_money1': operation_money1,
        })
    else:
        return redirect('main')
#создание++\редактирование++##gospodi perepishi eto der'mo, eto 妈的笔啥都看不懂，以后要改修\gengxin的时候可以发现问题
def trading_operation_cashbox_manage(request):
    if request.user.is_staff or request.user.is_superuser:
        cashbox_id = request.GET.get('cashbox_id', '')
        type = request.GET.get('type', 'create')
        object = request.GET.get('object', 'plus')
        editformset1 = modelformset_factory(operation_product_cashbox_instance, form=operation_product_cashbox_instanceForm, extra = 1) 
        #type_operation_money_sort = product.objects.filter(amount0__gt=0)
        cashbox1 = get_object_or_404(cashbox_mm, pk=cashbox_id)
        if cashbox1.admin_cashbox is True and request.user.is_superuser is not True:
            return print('cashbox1.admin_cashbox is True and request.user.is_superuser is not True')
        #create
        if type == "create":
            if request.method == "POST":
                form = operation_moneyForm(request.POST)
                form.fields["type"].queryset = type_operation_money_mm.filter(type=object)
                if object == "minusplus":
                    del form.fields["client"]
                else:
                    del form.fields["cashbox_recieve"]
                editformset = editformset1(request.POST,  queryset=operation_product_cashbox_instance_mm.none(), prefix='payment')
                for kas in editformset:
                    del kas.fields["operation_money"]
                if form.is_valid() and editformset.is_valid():
                    operation_money = form.save(commit=False)
                    operation_money.cashbox = cashbox1
                    operation_money.created_date = timezone.now()
                    operation_type = operation_money.type
                    if operation_type.type == object:
                        if object == "plus":
                            if operation_type.type == 'plus':
                                cashbox1.cash = (cashbox1.cash + operation_money.cash)
                                operation_money.leftovers = operation_money.cash
                        if object == "minus":
                            if operation_type.type == 'minus':
                                cashbox1.cash = (cashbox1.cash - operation_money.cash)
                                operation_money.leftovers = operation_money.cash
                        if object == "minusplus":
                            if operation_type.type == 'minusplus':                        
                                cashbox1.cash = (cashbox1.cash - operation_money.cash)
                                operation_money.cashbox_recieve.cash = (operation_money.cashbox_recieve.cash + operation_money.cash)
                                operation_money.cashbox_recieve.save()
                                operation_money.leftovers = "0"
                        operation_money.save()
                        cashbox1.save()
                        for n in editformset:
                            if not n.empty_permitted:
                                payment_instance = n.save(commit=False)
                                payment_instance.cashbox = cashbox1
                                if payment_instance.operation_product is not None:
                                    if operation_money.type.type != payment_instance.operation_product.type.type:
                                        operation_money.leftovers = (operation_money.leftovers - payment_instance.cash)
                                        print (payment_instance.operation_product.leftovers)
                                        payment_instance.operation_product.leftovers = (payment_instance.operation_product.leftovers -  payment_instance.cash)
                                        print (payment_instance.operation_product.leftovers)
                                        payment_instance.operation_product.save()
                                        payment_instance.operation_money = operation_money
                                        payment_instance.save()                        
                                        operation_money.save()
                        memory_action.objects.create(name = operation_money.type.name, action = 'Создание ' + operation_money.type.name + ' на сумму ' + str(operation_money.cash) + ' в кассе ' + cashbox1.name, created_date = timezone.now())
                        ##костыль пздц
                        return redirect('/trading/operation_cashbox?cashbox=%s' % cashbox_id )
            else:
                form = operation_moneyForm()
                form.fields["type"].queryset = type_operation_money_mm.filter(type=object)
                form.fields["type"].empty_label=None
                if object == "minusplus":
                    del form.fields["client"]
                    form.fields["cashbox_recieve"].empty_label=None
                    form.fields["cashbox_recieve"].queryset = cashbox_mm.all().exclude(pk=cashbox1.pk)
                    form.fields["cashbox_recieve"].label = 'Касса получатель'
                    form.fields["cashbox_recieve"].widget.attrs.update({'class': 'form-control','placeholder':'Касса получатель'})
                else:
                    del form.fields["cashbox_recieve"]
                    form.fields["client"].empty_label=None
                    form.fields["client"].label = 'Клиент'
                    form.fields["client"].widget.attrs.update({'class': 'form-control','placeholder':'Клиент'})
                editformset = editformset1(queryset=operation_product_cashbox_instance_mm.none(), prefix='payment')
                for a in editformset:
                    del a.fields["cashbox"]
                    a.fields["operation_product"].label = ''
                    a.fields["cash"].label = ''
                    del a.fields["operation_money"]
                    #mb ne proidet
                    a.fields["operation_product"].queryset = operation_product_mm.filter()
                    fields = list(a)
                    a.part1, a.part2,a.part3 = fields[0], fields[1],fields[2:]
                    fields= None
                form.fields["created_date"].label = 'Дата'
                form.fields["created_date"].widget.attrs.update({'class': 'form-control','placeholder':'Дата'})
                form.fields["type"].label = 'Вид операции'
                form.fields["type"].widget.attrs.update({'class': 'form-control','placeholder':'Вид операции'})
                form.fields["cash"].label = 'Сумма'
                form.fields["cash"].widget.attrs.update({'class': 'form-control','placeholder':'Сумма'})
                form.fields["commentary"].label = 'Примечание'
                form.fields["commentary"].widget.attrs.update({'class': 'form-control','rows':"3",'placeholder':'Примечание'})
                
            return render(request, 'automaximum/trading_operation_cashbox_manage.html', {
            'nav_bar' : 'trading_operation_cashbox',
            'cashbox1': cashbox1,
            'editformset': editformset,
            'form': form,
            'page': 'create',
            })
        #edit
        if type == "edit":
            operation_id = request.GET.get('operation_id', '')
            operation_money1 = get_object_or_404(operation_money_mm, pk=operation_id)
            operation_money_backup = operation_money_mm.get(pk=operation_money1.pk)
            operation_product_cashbox_instance_backup = operation_product_cashbox_instance_mm.filter(operation_money=operation_money1)
            if request.method == "POST":
                form = operation_moneyForm(request.POST, instance=operation_money1)
                if object == "minusplus":
                    del form.fields["client"]
                else:
                    del form.fields["cashbox_recieve"]
                editformset = editformset1(request.POST,  queryset=operation_product_cashbox_instance_mm.filter(operation_money=operation_money1), prefix='payment')
                for d in editformset:
                    del d.fields["cashbox"]
                    del d.fields["operation_money"]
                delme = None
                if request.POST.get('deleteit', '') == 'true':
                    delme = "smth"
                #formset dlya platejei    
                if form.is_valid() and editformset.is_valid():
                    operation_money1 = form.save(commit=False)
                    #proverka na podmenu post
                    if operation_money1.cashbox == operation_money1.cashbox_recieve:
                        return redirect('/trading/operation_cashbox/list?cashbox=%s' % operation_money1.cashbox.pk )
                    if operation_money1.type.type == operation_money_backup.type.type:
                        if operation_money1.cashbox != operation_money_backup.cashbox:
                            return redirect('/trading/operation_cashbox/list?cashbox=%s' % operation_money1.cashbox.pk )
                        operation_type = operation_money_backup.type
                        if operation_type.type == 'plus':
                            cashbox1.cash = (cashbox1.cash - operation_money_backup.cash)
                        if operation_type.type == 'minus':
                            cashbox1.cash = (cashbox1.cash + operation_money_backup.cash)
                        if operation_type.type == 'minusplus':
                            cashbox1.cash = (cashbox1.cash + operation_money_backup.cash)
                            operation_money_backup.cashbox_recieve.cash = (operation_money_backup.cashbox_recieve.cash - operation_money_backup.cash)                         
                        #spisivaniye s kass
                        #reset leftovers
                        if delme is None:
                            operation_money1.leftovers = operation_money1.cash                        
                            operation_type1 = operation_money1.type
                            if operation_type1.type == 'plus':
                                cashbox1.cash = (cashbox1.cash + operation_money1.cash)
                            if operation_type1.type == 'minus':
                                cashbox1.cash = (cashbox1.cash - operation_money1.cash)
                            if operation_type1.type == 'minusplus':                        
                                cashbox1.cash = (cashbox1.cash - operation_money1.cash)
                                if operation_money1.cashbox_recieve == operation_money_backup.cashbox_recieve:
                                    operation_money_backup.cashbox_recieve.cash = (operation_money_backup.cashbox_recieve.cash + operation_money1.cash)
                                else:
                                    operation_money1.cashbox_recieve.cash = (operation_money1.cashbox_recieve.cash + operation_money1.cash)
                                    operation_money1.cashbox_recieve.save()
                                operation_money_backup.cashbox_recieve.save()
                                operation_money1.leftovers = "0"
                        cashbox1.save()
                        #formset dlya platejei
                        

                        #esli eto ne proidet, to sdelai save cherez operation_money1, t.k on zadaetsa instansom
                        
                        for c in editformset:
                            if not c.empty_permitted:
                                payment_instancez = c.save(commit=False)
                                if payment_instancez.operation_product is not None:
                                    if operation_money1.type.type != payment_instancez.operation_product.type.type:
                                        operation_money1.leftovers = (operation_money1.leftovers - payment_instancez.cash)
                                        for instance_backup in operation_product_cashbox_instance_backup:
                                            if payment_instancez.pk == instance_backup.pk:
                                                zz1 = operation_product_cashbox_instance_mm.get(pk=payment_instancez.pk)
                                                payment_instancez.operation_product.leftovers = (payment_instancez.operation_product.leftovers + zz1.cash)
                                        if delme == "smth":
                                            payment_instancez.delete()
                                        else:
                                            payment_instancez.operation_product.leftovers = (payment_instancez.operation_product.leftovers -  payment_instancez.cash)
                                            payment_instancez.operation_money = operation_money1
                                            payment_instancez.cashbox = cashbox1                                            
                                            payment_instancez.save()
                                        payment_instancez.operation_product.save()
                        if delme == "smth":
                            operation_money1.delete()
                        else:   
                            operation_money1.save()
                        #arhiv
                        memory_action.objects.create(name = operation_money1.type.name, action = 'Редактирование ' + operation_money_backup.type.name + ' ' , created_date = timezone.now())
                        ###костыль
                        return redirect('/trading/operation_cashbox?cashbox=%s' % operation_money1.cashbox.pk )                    

            else:
                form = operation_moneyForm(instance=operation_money1)
                form.fields["type"].queryset = type_operation_money.objects.filter(type=object)
                form.fields["type"].empty_label=None
                if object == "minusplus":
                    del form.fields["client"]
                    form.fields["cashbox_recieve"].empty_label=None
                    form.fields["cashbox_recieve"].queryset = cashbox_mm.all().exclude(pk=cashbox1.pk)
                    form.fields["cashbox_recieve"].label = 'Касса получатель'
                    form.fields["cashbox_recieve"].widget.attrs.update({'class': 'form-control','placeholder':'Касса получатель'})
                else:
                    del form.fields["cashbox_recieve"]
                    form.fields["client"].empty_label=None
                    form.fields["client"].label = 'Клиент'
                    form.fields["client"].widget.attrs.update({'class': 'form-control','placeholder':'Клиент'})
                #formset dlya platejei
                editformset = editformset1(queryset=operation_product_cashbox_instance_mm.filter(operation_money=operation_money1), prefix='payment')
                for d in editformset:
                    del d.fields["cashbox"]
                    del d.fields["operation_money"]
                    d.fields["operation_product"].label = ''
                    d.fields["cash"].label = ''
                    fields = list(d)
                    d.part1, d.part2 = fields[0], fields[1]
                    fields= None
                    #mb ne proidet
                    #d.fields["operation_product"].queryset = operation_product_mm.filter(type=object)
                #krasotisha!
                form.fields["created_date"].label = 'Дата'
                form.fields["created_date"].widget.attrs.update({'class': 'form-control','placeholder':'Дата'})
                form.fields["type"].label = 'Вид операции'
                form.fields["type"].widget.attrs.update({'class': 'form-control','placeholder':'Вид операции'})
                form.fields["cash"].label = 'Сумма'
                form.fields["cash"].widget.attrs.update({'class': 'form-control','placeholder':'Сумма'})
                form.fields["commentary"].label = 'Примечание'
                form.fields["commentary"].widget.attrs.update({'class': 'form-control','rows':"3",'placeholder':'Примечание'})
                return render(request, 'automaximum/trading_operation_cashbox_manage.html', {
                'nav_bar' : 'trading_operation_cashbox',
                'operation_money1': operation_money1,
                'editformset': editformset,
                'cashbox1': cashbox1,
                'form': form,
                'page': 'edit',
                })
                
            
    #if not staff\superuser        
    else:
        return redirect('main')
#просмотр
def trading_operation_cashbox_view(request):
    if request.user.is_staff or request.user.is_superuser:
        operation_money1 = get_object_or_404(operation_money,pk=request.GET.get('id'))
        return render(request, 'automaximum/trading_operation_cashbox_view.html', {
        'nav_bar' : 'trading_operation_cashbox',
        'operation_money1': operation_money1,
        })
    else:
        return redirect('main')


#товарные операции
def trading_operation_product(request):
    if request.user.is_staff or request.user.is_superuser:
        type_operation_product_all = type_operation_product.objects.all().order_by('name')
        sort_type = request.GET.get('sort_type', '')
        if sort_type == '':
            type_operation_product1 = type_operation_product.objects.all()[0]
        else:
            type_operation_product1 = get_object_or_404(type_operation_product, pk=sort_type)
        operation_product1 = operation_product.objects.filter(type=type_operation_product1).order_by('-created_date')
        return render(request, 'automaximum/trading_operation_product.html', {
        'nav_bar' : 'trading_operation_product',
        'type_operation_product_all': type_operation_product_all,
        'operation_product1': operation_product1,
        'type_operation_product1': type_operation_product1,
        'sort_type': sort_type,
        })
    else:
        return redirect('main')
#просмотр товарной операции
def trading_operation_product_view(request):
    if request.user.is_staff or request.user.is_superuser:
        id = request.GET.get('id', '')
        if id:
            operation_product1 = get_object_or_404(operation_product, pk=id)
            return render(request, 'automaximum/trading_operation_product_view.html', {
            'nav_bar' : 'trading_operation_product',
            'operation_product1': operation_product1,
            })
        else: 
            return redirect('trading_operation_products')
    else:
        return redirect('main')
##gospodi perepishi eto der'mo, eto 妈的笔啥都看不懂，以后要改修\gengxin的时候可以发现问题
def trading_operation_product_create(request):
    if request.user.is_staff or request.user.is_superuser:
        init = request.GET.get('init', '')
        userstaff = request.user
        if init == 'val':
            kiss = trading_product_in_basket.objects.filter(user=userstaff)
        operation_id = request.GET.get('operation_id', '')
        editformset1 = modelformset_factory(operation_product_product_instance, form=operation_product_product_instanceForm, extra = 1)    
        editformset2 = modelformset_factory(operation_product_cashbox_instance, form=operation_product_cashbox_instanceForm, extra = 1)  
        operation_product1 = get_object_or_404(type_operation_product, pk=operation_id)        
        if request.method == "POST":    
            form = operation_productForm(request.POST)
            if operation_product1.type == "minusplus":
                del form.fields["client"]
            else:
                del form.fields["storage_recieve"]
            if operation_product1.changes_price == True:
                del form.fields["price"]
            
            editformset = editformset1(request.POST,  queryset=operation_product_product_instance.objects.none())
            editformset_cashbox = editformset2(request.POST, queryset=operation_product_cashbox_instance.objects.none(), prefix='cashbox')
            for sdf in editformset_cashbox:
                sdf.fields["cashbox"].queryset = cashbox.objects.filter(admin_cashbox=False)
            spisaniye = None
            if request.POST.get('approved', '') == 'true':
                spisaniye = "smth"
            if request.user.is_superuser:
                None
            else:
                for arms in editformset:
                    if operation_product1.type != "minusplus" and operation_product1.changes_price == False:
                        del arms.fields["product_price"]
                del form.fields["car"]
            if form.is_valid() and editformset.is_valid() and editformset_cashbox.is_valid():
                print('poehali')
                operation_product = form.save()
                operation_product.type = operation_product1
                #spisaniye
                if spisaniye != None:
                    operation_product.approved = True
                operation_product.cash = 0                
                for z in editformset:
                    #我不懂这个是咋做的，要更新跳过
                        operation_product_product_instancez = z.save()
                        if operation_product_product_instancez.product is not None:
                            if operation_product.type != "minusplus" and operation_product1.changes_price == False and not request.user.is_superuser:
                                operation_product_product_instancez.product_price = price_value.objects.get(price=operation_product.price, product = operation_product_product_instancez.product).value
                            operation_product_product_instancez.product.deletefree = False
                            if operation_product.type.type != 'minusplus' and operation_product_product_instancez.product_amount and operation_product_product_instancez.product_price:
                                operation_product.cash = (operation_product.cash + (operation_product_product_instancez.product_price * operation_product_product_instancez.product_amount))
                            operation_product_product_instancez.operation_product = operation_product
                            if operation_product.type.type == 'plus':
                                if operation_product.approved == True:
                                    operation_product_product_instancez.product.amount0 = (operation_product_product_instancez.product.amount0 + operation_product_product_instancez.product_amount)
                                    if operation_product.type.changes_price == True and operation_product_product_instancez.product_price:
                                        operation_product_product_instancez.product.price0 = operation_product_product_instancez.product_price
                                    product_amount = amount_on_storage.objects.get(product = operation_product_product_instancez.product, storage = operation_product.storage)
                                    product_amount.amount = (product_amount.amount + operation_product_product_instancez.product_amount)
                                    operation_product_product_instancez.product.save()
                                    #这个是为更新推荐价格的那个部分
                                    if operation_product.type.changes_price == True:                                        
                                        for ias in price_value.objects.filter(product=operation_product_product_instancez.product):
                                            ias.save()
                            if operation_product.type.type == 'minus':
                                if operation_product.approved == True:
                                    operation_product_product_instancez.product.amount0 = (operation_product_product_instancez.product.amount0 - operation_product_product_instancez.product_amount)
                                    product_amount = amount_on_storage.objects.get(product = operation_product_product_instancez.product, storage = operation_product.storage)
                                    product_amount.amount = (product_amount.amount - operation_product_product_instancez.product_amount)
                                    operation_product_product_instancez.product.save()
                            if operation_product.type.type == 'minusplus':
                                if operation_product.approved == True:
                                    product_amount = amount_on_storage.objects.get(product = operation_product_product_instancez.product, storage = operation_product.storage)
                                    product_amount.amount = (product_amount.amount - operation_product_product_instancez.product_amount)
                                    product_amount1 = amount_on_storage.objects.get(product = operation_product_product_instancez.product, storage = operation_product.storage_recieve)
                                    product_amount1.amount = (product_amount1.amount + operation_product_product_instancez.product_amount)
                                    product_amount1.save()
                            if operation_product.approved == True:
                                product_amount.save()
                            operation_product_product_instancez.product.save()
                            operation_product_product_instancez.created_date = operation_product.created_date
                            operation_product_product_instancez.save()
                operation_product.leftovers = operation_product.cash
                for y in editformset_cashbox:
                    operation_product_cashbox_instancez = y.save(commit=False)
                    if operation_product_cashbox_instancez.cashbox is not None and operation_product_cashbox_instancez.cash != 0:
                        operation_money_create = operation_money.objects.create(type = operation_product.type.creates, cash = operation_product_cashbox_instancez.cash, cashbox = operation_product_cashbox_instancez.cashbox, client = operation_product.client, leftovers = "0")
                        operation_money_create_cashbox = operation_money_create.cashbox
                        if operation_money_create.type.type == 'plus':
                            operation_money_create_cashbox.cash = (operation_money_create_cashbox.cash + operation_money_create.cash)
                        if operation_money_create.type.type == 'minus':
                            operation_money_create_cashbox.cash = (operation_money_create_cashbox.cash + operation_money_create.cash)
                        operation_money_create_cashbox.save()
                        operation_product_cashbox_instancez.operation_money = operation_money_create
                        operation_product_cashbox_instancez.operation_product = operation_product
                        operation_product.leftovers = (operation_product.leftovers - operation_product_cashbox_instancez.cash)
                        operation_product_cashbox_instancez.save()
                
                operation_product.save()
                if init == 'val':
                    removeitemsfrombasket(userstaff.pk)
                return redirect('/trading/operation_product/list?sort_type=%s' % operation_product.type.pk )                              
            else:
                print('sa')
        else:
            #obrabativaem formu
            form = operation_productForm()
            del form.fields["car"]
            form.fields["price"].empty_label=None
            form.fields["created_by"].empty_label=None
            form.fields["created_by"].queryset = User.objects.filter(Q(is_staff=True)| Q(is_superuser=True))
            form.fields["created_by"].initial=request.user
            form.fields["storage"].empty_label=None
            #defoltniye znacheniya
            if operation_product1.default_price != None:
                form['price'].initial = operation_product1.default_price
            if operation_product1.default_client != None:
                form['client'].initial = operation_product1.default_client
            #tip operacii
            var_for_form = None
            if operation_product1.type == "minusplus":
                del form.fields["price"]
                del form.fields["client"]
                form.fields["storage_recieve"].empty_label=None
                var_for_form = 'smth'
            else:
                del form.fields["storage_recieve"]
                form.fields["client"].empty_label=None
            if operation_product1.changes_price == True:
                del form.fields["price"]
            #obrabativaem editformset
            if init == 'val':
                editformset = editformset1(queryset=kiss)
            else:
                editformset = editformset1(queryset=operation_product_product_instance.objects.none())
            for arms in editformset:
                if operation_product1.type == "minusplus":
                    del arms.fields["product_price"]
                if arms.instance.product != None:
                    zae = kiss.get(product=arms.instance.product)
                    arms['product_amount'].initial = float(zae.value)
                fields = list(arms)
                arms.part0, arms.part1, arms.part2 = fields[0], fields[1], fields[2]
            #obrabativaem editformsetcashbox
            editformset_cashbox = editformset2(queryset=operation_product_cashbox_instance.objects.none(), prefix='cashbox')
            for vcv in editformset_cashbox:
                vcv.fields["cashbox"].label = ''
                vcv.fields["cash"].label = ''
                del vcv.fields["operation_product"]
                del vcv.fields["operation_money"]
                vcv.fields["cashbox"].queryset = cashbox.objects.filter(admin_cashbox=False)
                fields = list(vcv)
                vcv.part1, vcv.part2 = fields[0], fields[1]
                fields= None
            #要看谁来干
            if request.user.is_superuser:
                None
            else:
                for arms in editformset:
                    if operation_product1.type != "minusplus" and operation_product1.changes_price == False:
                        arms.fields["product_price"].widget.attrs.update({'readonly': ''})
                del form.fields["car"]
            return render(request, 'automaximum/trading_operation_product_create.html', {
            'nav_bar' : 'trading_operation_product',
            'editformset': editformset,
            'editformset_cashbox': editformset_cashbox,
            'form': form,
            'operation_product1': operation_product1,
            'page' : 'new',
            'var_for_form': var_for_form,
            })
    else:
        return redirect('main')

def trading_operation_product_edit(request):
    if request.user.is_staff or request.user.is_superuser:
        userstaff = request.user
        operation_id = request.GET.get('operation_id', '')
        editformset1 = modelformset_factory(operation_product_product_instance, form=operation_product_product_instanceForm, extra = 1)    
        editformset2 = modelformset_factory(operation_product_cashbox_instance, form=operation_product_cashbox_instanceForm, extra = 1) 
        editformset3 = modelformset_factory(operation_product_cashbox_instance, form=operation_product_cashbox_instanceForm, extra = 0)        
        operation_product1 = get_object_or_404(operation_product_mm, pk=operation_id)
        operation_product1_backup = operation_product_mm.get(pk = operation_product1.pk)
        operation_product1_instance_backup = operation_product_product_instance_mm.filter(operation_product = operation_product1)
        operation_product1_payment_backup = operation_product_cashbox_instance_mm.filter(operation_product = operation_product1)
        if request.method == "POST":
            form = operation_productForm(request.POST, instance = operation_product1)
            if operation_product1.type.type == "minusplus":
                del form.fields["client"]
            else:
                del form.fields["storage_recieve"]
            if operation_product1.type.changes_price == True:
                del form.fields["price"]
            editformset = editformset1(request.POST,  queryset=operation_product_product_instance.objects.filter(operation_product = operation_product1))
            editformset_cashbox = editformset2(request.POST,queryset=operation_product_cashbox_instance.objects.none(), prefix='cashbox')
            for sdf in editformset_cashbox:
                sdf.fields["cashbox"].queryset = cashbox.objects.filter(admin_cashbox=False)
                del sdf.fields["operation_product"]
                del sdf.fields["operation_money"]
            editformset_payment_edit = editformset3(request.POST,queryset=operation_product_cashbox_instance.objects.filter(operation_product = operation_product1), prefix='payment')
            for eqe in editformset_payment_edit:
                del eqe.fields["cashbox"]
                del eqe.fields["operation_money"]
                del eqe.fields["operation_product"]
            #tut berem informaciyu o provedenii
            spisaniye = None
            if request.POST.get('approved', '') == 'true':
                spisaniye = "smth"
            delme = None
            if request.POST.get('deleteit', '') == 'true':
                delme = "smth"
            if request.user.is_superuser:
                None
            else:
                for arms in editformset:
                    if operation_product1.type.type != "minusplus" and operation_product1.type.changes_price == False:
                        del arms.fields["product_price"]
            if form.is_valid() and editformset.is_valid() and editformset_cashbox.is_valid() and editformset_payment_edit.is_valid():
                print('####################form vali')
                operation_product1 = form.save()
                operation_product1.cash = 0
                if operation_product1_backup.approved == True:
                    for items in operation_product1_instance_backup:
                        product_restore = amount_on_storage.objects.get(product = items.product, storage = operation_product1_backup.storage)
                        if operation_product1_backup.type.type == 'plus':
                            product_restore.amount = (product_restore.amount - items.product_amount)
                            items.product.amount0 = (items.product.amount0 - items.product_amount)
                            items.product.save()
                        if operation_product1_backup.type.type == 'minus':
                            product_restore.amount = (product_restore.amount + items.product_amount)
                            items.product.amount0 = (items.product.amount0 + items.product_amount)
                            items.product.save()
                        if operation_product1_backup.type.type == 'minusplus':
                            product_restore.amount = (product_restore.amount + items.product_amount)
                            product_restore_recieve = amount_on_storage.objects.get(product = items.product, storage = operation_product1_backup.storage_recieve)
                            product_restore_recieve.amount = (product_restore_recieve.amount - items.product_amount)
                            product_restore_recieve.save()
                        product_restore.save()
                        if delme == "smth":
                            items.delete()
                if spisaniye:
                    operation_product1.approved = True
                for form in editformset:
                    if delme == "smth":
                        None
                    else:
                        operation_product_product_instancez = form.save(commit=False)
                        if operation_product_product_instancez.product is not None:
                            operation_product_product_instancez.product.deletefree = False
                            if operation_product1.type.type != "minusplus" and operation_product1.type.changes_price == False and not request.user.is_superuser:
                                operation_product_product_instancez.product_price = price_value.objects.get(price=operation_product1.price, product = operation_product_product_instancez.product).value
                            operation_product_product_instancez_product = product.objects.get(pk = operation_product_product_instancez.product.pk)
                            operation_product_product_instancez.product.amount0 = operation_product_product_instancez_product.amount0
                            if operation_product1.type.type != 'minusplus' and operation_product_product_instancez.product_amount and operation_product_product_instancez.product_price:
                                operation_product1.cash = (operation_product1.cash + (operation_product_product_instancez.product_price * operation_product_product_instancez.product_amount))
                            operation_product_product_instancez.operation_product = operation_product1
                            if operation_product1.type.type == 'plus':
                                if operation_product1.approved == True:
                                    if operation_product1.type.changes_price == True and operation_product_product_instancez.product_price:
                                        operation_product_product_instancez.product.price0 = operation_product_product_instancez.product_price
                                    product_amount = amount_on_storage.objects.get(product = operation_product_product_instancez.product, storage = operation_product1.storage)
                                    product_amount.amount = (product_amount.amount + operation_product_product_instancez.product_amount)
                                    operation_product_product_instancez.product.amount0 = (operation_product_product_instancez.product.amount0 +  operation_product_product_instancez.product_amount)
                                    operation_product_product_instancez.product.save()
                                    if operation_product1.type.changes_price == True:
                                        for ias in price_value.objects.filter(product=operation_product_product_instancez.product):
                                            ias.save()
                                    product_amount.save()
                            if operation_product1.type.type == 'minus':
                                if operation_product1.approved == True:
                                    product_amount = amount_on_storage.objects.get(product = operation_product_product_instancez.product, storage = operation_product1.storage)
                                    product_amount.amount = (product_amount.amount - operation_product_product_instancez.product_amount)
                                    operation_product_product_instancez.product.amount0 = (operation_product_product_instancez.product.amount0 -  operation_product_product_instancez.product_amount)
                                    operation_product_product_instancez.product.save()
                                    product_amount.save()
                            if operation_product1.type.type == 'minusplus':
                                if operation_product1.approved == True:
                                    product_amount = amount_on_storage.objects.get(product = operation_product_product_instancez.product, storage = operation_product1.storage)
                                    product_amount.amount = (product_amount.amount - operation_product_product_instancez.product_amount)
                                    product_recieve = amount_on_storage.objects.get(product = operation_product_product_instancez.product, storage = operation_product1.storage_recieve)
                                    product_recieve.amount = (product_recieve.amount + operation_product_product_instancez.product_amount)
                                    product_recieve.save()
                                    product_amount.save()
                            operation_product_product_instancez.created_date = operation_product1.created_date
                            operation_product_product_instancez.product.deletefree = False
                            operation_product_product_instancez.product.save()
                            operation_product_product_instancez.save()
                        else:
                            if operation_product_product_instancez.pk != None:
                                operation_product_product_instancez.delete()
                #ostatki
                operation_product1.leftovers = operation_product1.cash
                #пересчет остатков leftovers
                #operation_product1.cash        
                #sozdaniye oplati
                for hgf in editformset_cashbox:
                    if delme is None:
                    #if not hgf.empty_permitted:
                        operation_product_cashbox_instancez = hgf.save(commit=False)
                        if operation_product_cashbox_instancez.cashbox and operation_product_cashbox_instancez.cash != 0:
                            operation_money_create = operation_money.objects.create(type = operation_product1.type.creates, cash = operation_product_cashbox_instancez.cash, cashbox = operation_product_cashbox_instancez.cashbox, client = operation_product1.client, leftovers = "0")
                            operation_money_create_cashbox = operation_money_create.cashbox
                            if operation_money_create.type.type == 'plus':
                                operation_money_create_cashbox.cash = (operation_money_create_cashbox.cash + operation_money_create.cash)
                            if operation_money_create.type.type == 'minus':
                                operation_money_create_cashbox.cash = (operation_money_create_cashbox.cash - operation_money_create.cash)
                            operation_money_create_cashbox.save()
                            operation_product_cashbox_instancez.operation_money = operation_money_create
                            operation_product_cashbox_instancez.operation_product = operation_product1
                            operation_product1.leftovers = (operation_product1.leftovers - operation_product_cashbox_instancez.cash)
                            operation_product_cashbox_instancez.save()
                #redaktirovaniye platejei
                for yte in editformset_payment_edit:
                    if not yte.empty_permitted:
                        edit_payment = yte.save(commit=False)
                        edit_payment_backup = operation_product_cashbox_instance_mm.get(pk = edit_payment.pk)
                        operation_product1.leftovers = (operation_product1.leftovers - edit_payment.cash)
                        edit_payment.operation_money.leftovers = (edit_payment.operation_money.leftovers + edit_payment_backup.cash)
                        if delme == "smth":
                            edit_payment.delete()
                        else:
                            edit_payment.operation_money.leftovers = (edit_payment.operation_money.leftovers - edit_payment.cash)
                            edit_payment.operation_money.save()
                            edit_payment.save()
                if delme == "smth":
                    operation_product1.delete()
                else:
                    operation_product1.save()                  
                return redirect('/trading/operation_product/list?sort_type=%s' % operation_product1.type.pk )   
            else:
                print('####################form invali')
        else:
            form = operation_productForm(instance = operation_product1)
            del form.fields["car"]
            form.fields["client"].empty_label=None
            form.fields["created_by"].empty_label=None
            form.fields["created_by"].queryset = User.objects.filter(Q(is_staff=True)| Q(is_superuser=True))
            form.fields["storage"].empty_label=None
            form.fields["price"].empty_label=None
            var_for_form = None
            if operation_product1.type.type == "minusplus":
                var_for_form = 'smth'
                del form.fields["price"]
                del form.fields["client"]
                form.fields["storage_recieve"].empty_label=None
            else:
                del form.fields["storage_recieve"]
                form.fields["client"].empty_label=None
            editformset = editformset1(queryset=operation_product_product_instance.objects.filter(operation_product = operation_product1))
            if operation_product1.type.type == "minusplus":
                for zbv in editformset:
                    del zbv.fields["product_price"]
            editformset_cashbox = editformset2(queryset=operation_product_cashbox_instance.objects.none(), prefix='cashbox')
            for vcv in editformset_cashbox:
                vcv.fields["cashbox"].label = ''
                vcv.fields["cash"].label = ''
                del vcv.fields["operation_product"]
                del vcv.fields["operation_money"]
                vcv.fields["cashbox"].queryset = cashbox.objects.filter(admin_cashbox=False)
                fields = list(vcv)
                vcv.part1, vcv.part2 = fields[0], fields[1]
                fields= None
            editformset_payment_edit = editformset3(queryset=operation_product_cashbox_instance.objects.filter(operation_product = operation_product1), prefix='payment')
            for asdz in editformset_payment_edit:
                del asdz.fields["cashbox"]
                asdz.fields["cash"].label = ''
                del asdz.fields["operation_money"]
                del asdz.fields["operation_product"]
                fields = list(asdz)
                asdz.part1 = fields[0]
                fields= None  
            for arms in editformset:
                arms.ttlprc = None
                if arms.instance.product and operation_product1.type.type != 'minusplus':
                    arms.ttlprc = (arms.instance.product_amount *arms.instance.product_price)
                fields = list(arms)
                arms.part0, arms.part1, arms.part2 = fields[0], fields[1], fields[2]
                fields= None
            if operation_product1.type.changes_price == True:
                del form.fields["price"]
            #要看谁来干
            if request.user.is_superuser:
                None
            else:
                for arms in editformset:
                    if operation_product1.type.type != "minusplus" and operation_product1.type.changes_price == False:
                        arms.fields["product_price"].widget.attrs.update({'readonly': ''})
                del form.fields["car"]
            return render(request, 'automaximum/trading_operation_product_create.html', {
            'nav_bar' : 'trading_operation_product',
            'editformset': editformset,
            'editformset_cashbox': editformset_cashbox,
            'editformset_payment_edit': editformset_payment_edit,
            'form': form,
            'operation_product1': operation_product1,
            'page' : 'edit',
            'var_for_form':var_for_form,
            })
    else:
        return redirect('main')
            

