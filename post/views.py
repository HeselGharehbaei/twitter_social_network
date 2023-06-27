from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Post, Comment
from django.db.models import Q
from django.views import View


class PostView(View):
    def get(self, request, post_title):
        post= Post.objects.get(title= post_title)
        tags = post.tags.all()
        likes, likes_count = post.get_like()
        comments, comments_count = post.get_comments()
        images = post.get_image()
        return render(request, 'post.html', 
        {'post': post, 'tags': tags, 'likes_count': likes_count, 'likes': likes,
        'comments_count': comments_count, 'comments': comments, 'images': images})   


class SearchPostsView(View):
    def get(self, request):
        query = request.GET.get('q')
        posts = Post.objects.filter(Q(title__icontains=query))
        context = {'posts': posts}
        return render(request, 'search_post.html', context)


class DeletePostView(View):
    def get(self, request, post_title):
        Post.objects.get(title= post_title).delete()
        return redirect("post")


class DeleteCommentView(View):
    def get(self, request, comment_id):
        Comment.objects.get(id= comment_id).delete()
        return redirect("post")        