from django.shortcuts import render, redirect
from .models import Account, Follow
from post.models import Post
from django.db.models import Q
from django.views import View
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from .models import Account



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


class UserLoginView(View):


    my_form = LoginForm
    my_template = 'login.html'

    def get(self, request):
        form = self.my_form()
        context = {'form': form}
        return render(request, self.my_template, context)  


    def post(self, request):
        form = self.my_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user= authenticate(username=form.clean_name(), password= cd["password"])
            if user:
                login(request, user)
                messages.success(request, 'logging in successfully', 'success')
                return redirect("user:home")
        context = {'form': form}        
        return render(
           request, self.my_template, context) 


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logging out successfully', 'success')
        return redirect("user:home")


class UserRegistrationView(View):


    my_form = UserRegistrationForm
    my_template = 'register.html'


    def get(self, request):
        form = self.my_form()
        context = {'form': form}
        return render(request, self.my_template, context)  


    def post(self, request):
        form = self.my_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = Account.objects.create_user(cd["username"], cd["email"], cd["password"])
            messages.success(request, 'create user successfully', 'success') 
            return redirect("user:home")
        context = {'form': form}        
        return render(
           request, self.my_template, context)             



                       