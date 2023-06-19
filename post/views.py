from django.shortcuts import render
from .models import Post
from django.db.models import Q


def post(request, post_id):
    post= Post.objects.get(id= post_id)
    return render(request, 'post.html', {'post': post})   


def search_posts(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=query))
    context = {'posts': posts}
    return render(request, 'search_post.html', context)