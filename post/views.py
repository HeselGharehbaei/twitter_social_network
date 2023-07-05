from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from user.models import Account
from django.db.models import Q
from django.views import View
from django.contrib import messages
from .forms import CreatCommentForm, PostEditForm, AddPostForm


class PostView(View):
    def get(self, request, post_title):
        print(request.user)
        post= Post.objects.get(title= post_title)
        tags = post.tags.all()
        likes, likes_count = post.get_like()
        comments, comments_count = post.get_comments()
        images = post.get_image()
        return render(request, 'post/post.html', 
        {'post': post, 'tags': tags, 'likes_count': likes_count, 'likes': likes,
        'comments_count': comments_count, 'comments': comments, 'images': images})          


class SearchPostsView(View):
    def get(self, request):
        query = request.GET.get('q')
        posts = Post.objects.filter(Q(title__icontains=query))
        context = {'posts': posts}
        return render(request, 'post/search_post.html', context)


class DeletePostView(View):
    def get(self, request, post_title):
        Post.objects.get(title= post_title).delete()
        messages.success(request, 'post deleted successfully', 'success')
        return redirect("user:home")


class DeleteCommentView(View):
    def get(self, request, comment_id):
        Comment.objects.get(id= comment_id).delete()
        messages.success(request, 'comment deleted successfully', 'success')
        return redirect("user:home")   


class EditPostView(View):
    def get(self, request, post_title):
        post = Post.objects.get(title=post_title)
        form = PostEditForm(instance=post)
        return render(request, 'post/postedit.html', {'form': form})

    def post(self, request, post_title):
        post = Post.objects.get(title=post_title)
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            messages.success(request, 'post edited successfully', 'success')
            return redirect("user:home")
        return render(request, 'post/postedit.html', {'form': form})  


class CreatCommentView(View):


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


class CreatCommentForCommentView (View):


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


class AddPostView(View):


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



