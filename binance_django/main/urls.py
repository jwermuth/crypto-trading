from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    # These are more like binance python api enpoints
    path('get_account', views.get_account, name='get_account'),
    path('accounts', views.get_account, name='accounts'),
    path('get_asset_balance/<str:asset>', views.get_access_balance, name='get_asset_balance'),
    # '<int:question_id>/vote/',
    # These are rest like enpoints
    path('balances', views.get_account, name='balances'),
    path('balances/<str:asset>', views.get_access_balance, name='get_asset_balance'),
    path('save_account', views.save_account, name='save_account'),
]
