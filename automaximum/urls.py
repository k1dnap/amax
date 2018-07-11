from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.main, name = 'main'),
    url(r'^sign$', views.sign, name='sign'),
    url(r'^(?i)trading/$', views.trading, name = 'trading'),
    #operation_products_related
    url(r'^trading/operation_product/list$', views.trading_operation_product, name = 'trading_operation_product'),
    url(r'^trading/operation_product/view$', views.trading_operation_product_view, name = 'trading_operation_product_view'),
    url(r'^trading/operation_product/create$', views.trading_operation_product_create, name = 'trading_operation_product_create'),
    url(r'^trading/operation_product/edit$', views.trading_operation_product_edit, name = 'trading_operation_product_edit'),
    #operation_cashbox_related
    url(r'^trading/operation_cashbox$', views.trading_operation_cashbox, name = 'trading_operation_cashbox'),
    url(r'^trading/operation_cashbox/manage$', views.trading_operation_cashbox_manage, name='trading_operation_cashbox_manage'),
    url(r'^trading/operation_cashbox/view$', views.trading_operation_cashbox_view, name='trading_operation_cashbox_view'),
    #products_related
    url(r'^trading/products/list$', views.trading_products_list, name = 'trading_products_list'),
    url(r'^trading/products/create$', views.trading_products_create, name='trading_products_create'),
    url(r'^trading/products/view$', views.trading_products_view, name='trading_products_view'),
    url(r'^trading/products/edit$', views.trading_products_edit, name='trading_products_edit'),
    #settings
    url(r'^trading/settings$', views.trading_settings, name = 'trading_settings'),
    url(r'^trading/settings/view$', views.trading_settings_view, name = 'trading_settings_view'),
    url(r'^trading/settings/manage$', views.trading_settings_manage, name = 'trading_settings_manage'),
    
    #test
    url(r'^trading/ajax$', views.trading_ajax, name='trading_ajax'),    
    url(r'^trading/basket$', views.trading_addtobasket, name='trading_addtobasket'),
    url(r'^test/$', views.test, name = 'test'),

]

#url(r'^trading/settings/user/create$', views.trading_create_staff_user, name = 'trading_create_staff_user'),
#   url(r'^О-компании/$', views.about_us, name = 'about_us'),
#    url(r'^Контакты/$', views.contacts, name = 'contacts'),
#    url(r'^Контакты/Отправлено$', views.thanks, name = 'thanks'),
#    url(r'^Продукция/$', views.product_list, name='product_list'),
#    url(r'^Продукция/(?P<slug>[-\w\d]+)/$', views.cat_list, name='cat_list'),
#    url(r'^Продукция/(?P<slugcat>[-\w\d]+)/(?P<slugprod>[-\w\d]+)-(?P<pk>\d+)/$', views.product_detail, name='product_detail'),
