from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from user.models import Account
from django.db.models import Q
from django.views import View
from django.contrib import messages
from .forms import CreatCommentForm, PostEditForm, AddPostForm
from django.contrib.auth.mixins import LoginRequiredMixin


class PostView(View):
    def get(self, request, post_title):
        print(request.user)
        post= get_object_or_404(Post, title= post_title)
        return render(request, 'post/post_details_from_title.html', {'post': post})          


class SearchPostsView(View):
    def get(self, request):
        query = request.GET.get('q')
        posts = Post.objects.filter(Q(title__icontains=query))
        context = {'posts': posts}
        return render(request, 'post/search_post.html', context)


class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, post_title):
        get_object_or_404(Post, title= post_title).delete()
        messages.success(request, 'post deleted successfully', 'success')
        return redirect("user:home")


class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        get_object_or_404(Comment, id= comment_id).delete()
        messages.success(request, 'comment deleted successfully', 'success')
        return redirect("user:home")   


class EditPostView(LoginRequiredMixin, View):
    my_form = PostEditForm
    my_template = 'post/postedit.html'


    def setup(self, request, post_title):
        self.this_post = get_object_or_404(Post, title=post_title)
        return super().setup(request, post_title)


    def dispatch(self, request, post_title):
        if self.this_post.user.id != request.user.id:
            return redirect("user:home")
        return super().dispatch(request, post_title)        


    def get(self, request, post_title):
        form = self.my_form(instance=self.this_post)
        return render(request, self.my_template, {'form': form})


    def post(self, request, post_title):
        form = self.my_form(request.POST, request.FILES, instance=self.this_post)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            messages.success(request, 'post edited successfully', 'success')
            return redirect("user:home")
        return render(request, self.my_template, {'form': form})  


class CreatCommentView(LoginRequiredMixin, View):
    my_form = CreatCommentForm
    my_template = 'post/creat_comment.html'


    def get(self, request, post_title, account_username):
        post = Post.objects.get(title=post_title)
        user =Account.objects.get(username=account_username)
        form = self.my_form()
        context = {'form': form}
        return render(request, self.my_template, context)  


    def post(self, request, post_title, account_username):
        post = Post.objects.get(title=post_title)
        user =Account.objects.get(username=account_username)
        form = self.my_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment = Comment.objects.create(text= cd["text"], user= user, post = post)
            messages.success(request, 'create comment successfully', 'success') 
            return redirect("user:home")
        context = {'form': form}        
        return render(
           request, self.my_template, context)


class CreatCommentForCommentView(LoginRequiredMixin, View):
    my_form = CreatCommentForm
    my_template = 'post/creat_comment.html'


    def get(self, request, post_title, account_username, comment_id):
        post = Post.objects.get(title=post_title)
        user =Account.objects.get(username=account_username)
        comment = Comment.objects.get(id=comment_id)
        form = self.my_form()
        context = {'form': form}
        return render(request, self.my_template, context)  


    def post(self, request, post_title, account_username, comment_id):
        post = Post.objects.get(title=post_title)
        user =Account.objects.get(username=account_username)
        comment_base = Comment.objects.get(id=comment_id)
        form = self.my_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment = Comment.objects.create(text= cd["text"], user= user, post = post, parent =comment_base)
            messages.success(request, 'create comment successfully', 'success') 
            return redirect("user:home")
        context = {'form': form}        
        return render(
           request, self.my_template, context)


class AddPostView(LoginRequiredMixin, View):
    my_form = AddPostForm
    my_template = 'post/add_post.html'


    def get(self, request, account_username):
        user =Account.objects.get(username=account_username)
        form = self.my_form()
        context = {'form': form}
        return render(request, self.my_template, context)  


    def post(self, request, account_username):
        user =Account.objects.get(username=account_username)
        form = self.my_form(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            post = Post.objects.create(text= cd["text"], title= cd["title"], user= user)
            messages.success(request, 'create post successfully', 'success') 
            return redirect("user:posts of user", account_username= user)
        context = {'form': form}        
        return render(
           request, self.my_template, context)    



