from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    # path('', views.index, name='index'),
    # These are more like binance python api enpoints
#    path('get_account', views.get_account, name='get_account'),
#    path('accounts', views.get_account, name='accounts'),
#    path('get_asset_balance/<str:asset>', views.get_access_balance, name='get_asset_balance'),
#    # '<int:question_id>/vote/',
#    # These are rest like enpoints
#    path('balances', views.get_account, name='balances'),
#    path('balances/<str:asset>', views.get_access_balance, name='get_asset_balance'),
#    path('save_account', views.save_account, name='save_account'),

    # generic views
#    path('get_accounts', views.IndexView.as_view(), name='get_accounts'),
#    path('get_accounts/<int:pk>/', views.DetailView.as_view(), name='get_accounts_detail'),

    # print(pformat(client.get_all_orders(symbol=TradePairs.ETHBUSD)))
    # path('get_all_orders/<str:tradepair>/', views.get_all_orders_tradepair, name='get_all_orders_tradepair'),

    # path('orders/', views.IndexView.as_view(), name='createorder_list'),
    # path('orders/<int:pk>/', views.DetailView.as_view(), name='createorder_detail'),
    # path('orders/create_order/', views.create_order, name='createorder'),
    path('api/', views.api, name='api'),
    path('api/create_order', views.create_order, name='create_order'),
    path('api/get_all_orders/<str:symbol>', views.get_all_orders, name='get_all_orders'),
    path('api/get_open_orders/<str:symbol>', views.get_open_orders, name='get_open_orders'),
    path('api/get_account', views.get_account, name='get_account'),
    path('api/cancel_order/<str:symbol>/<str:order_id>', views.cancel_order, name='cancel_order')
]
