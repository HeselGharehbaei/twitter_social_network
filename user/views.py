from django.shortcuts import render
from .models import Account
from post.models import Post
from django.db.models import Q


def home_page(request):
    accounts_detailes = Account.objects.all()
    posts_detailes = Post.objects.all()
    return render(request, 'home.html', {'accounts_detailes': accounts_detailes, 'posts_detailes': posts_detailes} )


def account(request, account_username):
    accounts = Account.objects.get(username= account_username)
    return render(request, 'account.html', {'accounts': accounts})       


def search_accounts(request):
    query = request.GET.get('q')
    accounts = Account.objects.filter(Q(username__icontains=query))
    context = {'accounts': accounts}
    return render(request, 'search_account.html', context)