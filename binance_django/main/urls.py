from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_account', views.get_account, name='get_account'),
    path('accounts', views.get_account, name='get_account'),
    path('get_asset_balance/<str:asset>', views.get_access_balance, name='get_asset_balance'),
    # '<int:question_id>/vote/',
    path('balances', views.get_account, name='get_account'),
    path('balances/<str:asset>', views.get_access_balance, name='get_asset_balance'),
]
