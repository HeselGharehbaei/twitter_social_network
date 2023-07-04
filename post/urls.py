from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('post/<str:post_title>/', views.PostView.as_view(), name= 'post'),
    path('search/post', views.SearchPostsView.as_view(), name='search posts'),
    path('delete/post/<str:post_title>', views.DeletePostView.as_view(), name='delete post'),
    path('edit/post/<str:post_title>', views.EditPostView.as_view(), name='edit post'),
    path('delete/comment/<int:comment_id>', views.DeleteCommentView.as_view(), name='delete comment'),
    path('creat/comment/<str:post_title>/<str:account_username>', views.CreatCommentView.as_view(), name='create_comment')

]