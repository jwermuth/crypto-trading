from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_account', views.get_account, name='get_account'),
]
