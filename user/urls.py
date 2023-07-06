from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('account/<str:account_username>/', views.AccountView.as_view(), name= 'account'), 
    path('follow/<str:account_username>/', views.UserFollowView.as_view(), name= 'user follow'), 
    path('unfollow/<str:account_username>/', views.UserUnfollowView.as_view(), name= 'user unfollow'),  
    path('search/account', views.SearchAccountView.as_view(), name='search account'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('edit/profile/<str:account_username>/', views.UserEditProfileView.as_view(), name='edit profile'),
    path('profile/posts/<str:account_username>/', views.UserPostsView.as_view(), name='posts of user')


]
