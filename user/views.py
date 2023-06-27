from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Account, Follow
from post.models import Post
from django.db.models import Q
from django.views import View


class HomePageView(View):
    def get(self, request):
        accounts_detailes = Account.objects.all()
        posts_detailes = Post.objects.all()
        return render(request, 'home.html', {'accounts_detailes': accounts_detailes, 'posts_detailes': posts_detailes})

class AccountView(View):
    def get(self, request, account_username):
        accounts = Account.objects.get(username=account_username)
        following_count, following, followers_count, followers = accounts.get_followers_and_following()
        posts = accounts.post.all()
        return render(request, 'account.html', {'accounts': accounts, 'following_count': following_count, 'following': following, 'followers_count': followers_count, 'followers': followers, 'posts': posts})

class SearchAccountView(View):
    def get(self, request):
        query = request.GET.get('q')
        accounts = Account.objects.filter(Q(username__icontains=query))
        context = {'accounts': accounts}
        return render(request, 'search_account.html', context)