from django.urls import path
from . import views


urlpatterns = [
    path('post/<str:post_title>/', views.post, name= 'post'),
    path('search/post', views.search_posts, name='search posts'),
]