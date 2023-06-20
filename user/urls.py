from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('account/<str:account_username>/', views.account, name= 'account'),   
    path('search/account', views.search_accounts, name='search account'),
]