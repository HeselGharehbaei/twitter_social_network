from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('account/<str:account_username>/', views.AccountView.as_view(), name= 'account'),   
    path('search/account', views.SearchAccountView.as_view(), name='search account'),
]