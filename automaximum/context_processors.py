from .models import trading_product_in_basket, type_operation_product
from django.contrib.auth.models import User

def trading_basket_user_list(request):
    if request.user.is_staff or request.user.is_superuser:
        userstaff = request.user
        operation_types = type_operation_product.objects.all()
        trading_product_in_basket_list = trading_product_in_basket.objects.filter(user=userstaff)
        products_in_basket_count = trading_product_in_basket_list.count()
        return {
            'trading_product_in_basket_list': trading_product_in_basket_list,
            'userstaff': userstaff,
            'operation_types': operation_types,
            'products_in_basket_count': products_in_basket_count,
            }
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session["session_key"] = 123
            #re-apply value
            request.session.cycle_key()
        return {
            'session_key': session_key,
            }