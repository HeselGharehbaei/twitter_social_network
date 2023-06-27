from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('post/<str:post_title>/', views.PostView.as_view(), name= 'post'),
    path('search/post', views.SearchPostsView.as_view(), name='search posts'),
    path('delete/<str:post_title>', views.DeletePostView.as_view(), name='delete post'),
    path('deletecomment/<int:comment_id>', views.DeleteCommentView.as_view(), name='delete comment'),
]