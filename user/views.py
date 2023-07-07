from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Follow
from post.models import Post
from django.db.models import Q
from django.views import View
from .forms import LoginForm, UserRegistrationForm, UserEditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from .models import Account
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import SetPasswordForm


class HomePageView(View):
    def get(self, request):
        posts_detailes = Post.objects.exclude(is_archived =True)
        return render(request, 'user/home.html', {'posts_detailes': posts_detailes})


class AccountView(View):
    def get(self, request, account_username):
        account = Account.objects.get(username=account_username)
        if account.is_deleted:
            messages.error(request,'this account is deleted','danger')
            return redirect("user:home")
        else:    
            following_count, following, followers_count, followers = account.get_followers_and_following()
            return render(request, 'user/account.html', {'account': account, 'following_count': following_count, 'following': following, 'followers_count': followers_count, 'followers': followers})


class SearchAccountView(View):
    def get(self, request):
        query = request.GET.get('q')
        accounts = Account.objects.filter(Q(username__icontains=query))
        context = {'accounts': accounts}
        return render(request, 'user/search_account.html', context)


class UserLoginView(View):
    my_form = LoginForm
    my_template = 'user/login.html'

    def get(self, request):
        form = self.my_form()
        context = {'form': form}
        return render(request, self.my_template, context)  


    def post(self, request):
        form = self.my_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user= authenticate(username=form.clean_name(), password= cd["password"])
            if not user.is_deleted:
                login(request, user)
                messages.success(request, 'logging in successfully', 'success')
                return redirect("user:home")
        messages.success(request, 'Your account is deleted or not registred', 'danger')        
        context = {'form': form}        
        return render(
           request, self.my_template, context) 


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logging out successfully', 'success')
        return redirect("user:home")


class UserRegistrationView(View):
    my_form = UserRegistrationForm
    my_template = 'user/register.html'


    def get(self, request):
        form = self.my_form()
        context = {'form': form}
        return render(request, self.my_template, context)  


    def post(self, request):
        form = self.my_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = Account.objects.create_user(cd["username"], cd["email"], cd["password1"])
            messages.success(request, 'create user successfully', 'success') 
            return redirect("user:home")
        context = {'form': form}        
        return render(
           request, self.my_template, context)             


class UserEditProfileView(LoginRequiredMixin, View):
    my_form = UserEditProfileForm
    my_template = 'user/usereditprofile.html'   


    def setup(self, request, account_username):
        self.this_user = get_object_or_404(Account, username=account_username)
        return super().setup(request, account_username)


    def dispatch(self, request, account_username):
        if self.this_user.id != request.user.id:
            return redirect("user:home")
        return super().dispatch(request, account_username) 


    def get(self, request, account_username):
        form = self.my_form(instance=self.this_user)
        return render(request, self.my_template, {'form': form})
        

    def post(self, request, account_username):
        form = self.my_form(request.POST, request.FILES, instance=self.this_user)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            messages.success(request, 'your account updated successfully', 'success')
            return redirect("user:account", account_username=cd["username"])
        return render(request, self.my_template, {'form': form})


class UserPostsView(LoginRequiredMixin, View):
    def get(self, request, account_username):
        account = get_object_or_404(Account, username=account_username)
        posts_detailes = account.post.all()
        return render(request, 'post/user_post.html', {'posts_detailes': posts_detailes})


class UserFollowView(LoginRequiredMixin, View):
	def dispatch(self, request, account_username):
		account = get_object_or_404(Account, username=account_username)
		if account.id != request.user.id:
			return super().dispatch(request, account_username)
		else:
			messages.error(request,'you cant follow/unfollow your account','danger')
			return redirect('user:account', account_username)

	def get(self, request, account_username):
		account = get_object_or_404(Account, username=account_username)
		follow = Follow.objects.filter(from_user=request.user, to_user=account)
		if follow.exists():
			messages.error(request, 'you are already following this user', 'danger')
		else:
			Follow(from_user=request.user, to_user=account).save()
			messages.success(request, 'you followed this user', 'success')
		return redirect('user:account', account_username)


class UserUnfollowView(LoginRequiredMixin, View):
	def dispatch(self, request, account_username):
		account = get_object_or_404(Account, username=account_username)
		if account.id != request.user.id:
			return super().dispatch(request, account_username)
		else:
			messages.error(request,'you cant follow/unfollow your account','danger')
			return redirect('user:account', account_username)

	def get(self, request, account_username):
		account = get_object_or_404(Account, username=account_username)
		follow = Follow.objects.filter(from_user=request.user, to_user=account)
		if follow.exists():
			follow.delete()
			messages.success(request, 'you unfollowed this user', 'success')
		else:
			messages.error(request, 'you are not following this user', 'danger')
		return redirect('user:account', account_username)


class DeleteAccountView(LoginRequiredMixin, View):
    def dispatch(self, request, account_username):
        account = get_object_or_404(Account, username=account_username)
        if account.id == request.user.id:
            return super().dispatch(request, account_username)
        else:
            messages.error(request,'you cant delete this account','danger')
            return redirect('user:account', account_username)
    def get(self, request, account_username):
        account = get_object_or_404(Account, username=account_username).delete()
        messages.success(request, 'you deleted your account', 'success')      
        return redirect('user:home')


class ChangePasswordView(LoginRequiredMixin, View):
    my_form = SetPasswordForm
    my_template = 'user/change_password.html'   


    def setup(self, request, account_username):
        self.this_user = get_object_or_404(Account, username=account_username)
        return super().setup(request, account_username)


    def dispatch(self, request, account_username):
        if self.this_user.id != request.user.id:
            return redirect("user:home")
        return super().dispatch(request, account_username) 


    def get(self, request, account_username):
        form = self.my_form(user=request.user, data=request.POST or None)
        return render(request, self.my_template, {'form': form})
        

    def post(self, request, account_username):
        form = self.my_form(user=request.user, data=request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'you deleted your account', 'success')      
            return redirect('user:home')
        return render(request, self.my_template, {'form': form})

                       
