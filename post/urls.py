from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:post_id>/', views.post, name= 'post'),
    path('search/post', views.search_posts, name='search posts'),
]