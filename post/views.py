from django.shortcuts import render
from .models import Post
from django.db.models import Q


def post(request, post_title):
    post= Post.objects.get(title= post_title)
    return render(request, 'post.html', {'post': post})   


def search_posts(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=query))
    context = {'posts': posts}
    return render(request, 'search_post.html', context)