from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like, DisLike, Image, Tag
from user.models import Account
from django.db.models import Q
from django.views import View
from django.contrib import messages
from .forms import CreatCommentForm, PostForm, ImageForm, TagForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory


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
    my_post_form = PostForm
    my_formset_image = modelformset_factory(Image, form= ImageForm)
    my_formset_tag = modelformset_factory(Tag, form= TagForm)
    my_template = 'post/add_edit_post.html'


    def setup(self, request, post_title):
        self.this_post = get_object_or_404(Post, title=post_title)
        return super().setup(request, post_title)


    def dispatch(self, request, post_title):
        if self.this_post.user.id != request.user.id:
            return redirect("user:home")
        return super().dispatch(request, post_title)        


    def get(self, request, post_title):
        post_form = self.my_post_form(instance=self.this_post)
        formset_image = self.my_formset_image(queryset=self.this_post.image.all())
        formset_tag = self.my_formset_tag(queryset=self.this_post.tags.all())
        context = {'post_form': post_form, 'formset_image': formset_image, 'formset_tag': formset_tag}
        return render(request, self.my_template, context) 

        
    def post(self, request, post_title):
        post_form = self.my_post_form(request.POST, instance=self.this_post)
        formset_image = self.my_formset_image(request.POST, request.FILES, queryset=self.this_post.image.all())
        formset_tag = self.my_formset_tag(request.POST, queryset=self.this_post.tags.all())
        if post_form.is_valid() and formset_image.is_valid() and formset_tag.is_valid() :
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            formset_image.save()
            formset_tag.save()       
            messages.success(request, 'post edited successfully', 'success') 
            return redirect("user:posts of user", account_username= request.user)
        context = {'post_form': post_form, 'formset_image': formset_image, 'formset_tag': formset_tag}     
        return render(
           request, self.my_template, context)        


class CreatCommentView(LoginRequiredMixin, View):
    my_form = CreatCommentForm
    my_template = 'post/creat_comment.html'


    def get(self, request, post_title):
        post = Post.objects.get(title=post_title)
        form = self.my_form()
        context = {'form': form}
        return render(request, self.my_template, context)  


    def post(self, request, post_title):
        post = Post.objects.get(title=post_title)
        form = self.my_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment = Comment.objects.create(text= cd["text"], user= request.user, post = post)
            messages.success(request, 'create comment successfully', 'success') 
            return redirect("user:home")
        context = {'form': form}        
        return render(
           request, self.my_template, context)


class CreatCommentForCommentView(LoginRequiredMixin, View):
    my_form = CreatCommentForm
    my_template = 'post/creat_comment.html'


    def get(self, request, post_title, comment_id):
        post = Post.objects.get(title=post_title)
        comment = Comment.objects.get(id=comment_id)
        form = self.my_form()
        context = {'form': form}
        return render(request, self.my_template, context)  


    def post(self, request, post_title, comment_id):
        post = Post.objects.get(title=post_title)
        comment_base = Comment.objects.get(id=comment_id)
        form = self.my_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment = Comment.objects.create(text= cd["text"], user= request.user, post = post, parent =comment_base)
            messages.success(request, 'create comment successfully', 'success') 
            return redirect("user:home")
        context = {'form': form}        
        return render(
           request, self.my_template, context)


class AddPostView(LoginRequiredMixin, View):
    my_post_form = PostForm
    my_formset_image = modelformset_factory(Image, form= ImageForm)
    my_formset_tag = modelformset_factory(Tag, form= TagForm)
    my_template = 'post/add_edit_post.html'


    def get(self, request, account_username):
        user =Account.objects.get(username=account_username)
        post_form = self.my_post_form()
        formset_image = self.my_formset_image(queryset=Image.objects.none())
        formset_tag = self.my_formset_tag(queryset=Tag.objects.none())
        context = {'post_form': post_form, 'formset_image': formset_image, 'formset_tag': formset_tag}
        return render(request, self.my_template, context)  


    def post(self, request, account_username):
        user =Account.objects.get(username=account_username)
        post_form = self.my_post_form(request.POST)
        formset_image = self.my_formset_image(request.POST, request.FILES, queryset=Image.objects.none())
        formset_tag = self.my_formset_tag(request.POST, queryset=Tag.objects.none())
        if post_form.is_valid() and formset_image.is_valid() and formset_tag.is_valid() :
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            for form in formset_image.cleaned_data:
                if form:
                    image = form["image"]
                    photo = Image(post = post, image = image)
                    photo.save()
            for form in formset_tag.cleaned_data:
                if form:
                    name = form["name"]
                    tag = Tag(post = post, name = name)
                    tag.save()        
            messages.success(request, 'create post successfully', 'success') 
            return redirect("user:posts of user", account_username= user)
        context = {'post_form': post_form, 'formset_image': formset_image, 'formset_tag': formset_tag}     
        return render(
           request, self.my_template, context)    


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post= get_object_or_404(Post, id=post_id)
        like= Like.objects.filter(post=post, user=request.user)
        dislike= DisLike.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'you have already liked this post', 'danger')
        elif dislike.exists():
            dislike.delete()
            Like.objects.create(post=post, user=request.user)
            messages.success(request, 'you liked this post', 'success')
        else:
            Like.objects.create(post=post, user=request.user)
            messages.success(request, 'you liked this post', 'success')      
        return redirect('user:home')


class PostDisLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(post=post, user=request.user)
        dislike = DisLike.objects.filter(post=post, user=request.user)
        if dislike.exists():
            messages.error(request, 'you have already disliked this post', 'danger')
        elif like.exists():
            like.delete()
            DisLike.objects.create(post=post, user=request.user)
            messages.success(request, 'you disliked this post', 'success') 
        else:
            DisLike.objects.create(post=post, user=request.user)
            messages.success(request, 'you disliked this post', 'success')             
        return redirect('user:home')  


class EditCommentView(LoginRequiredMixin, View): 
    my_form = CreatCommentForm
    my_template = 'post/creat_comment.html'


    def setup(self, request, comment_id):
        self.this_comment = get_object_or_404(Comment, id=comment_id)
        return super().setup(request, comment_id)


    def dispatch(self, request, comment_id):
        if self.this_comment.user.id != request.user.id:
            return redirect("user:home")
        return super().dispatch(request, comment_id)        


    def get(self, request, comment_id):
        form = self.my_form(instance=self.this_comment)
        return render(request, self.my_template, {'form': form})


    def post(self, request, comment_id):
        form = self.my_form(request.POST, instance=self.this_comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'create comment successfully', 'success') 
            return redirect("user:home")
        context = {'form': form}        
        return render(
           request, self.my_template, context)                


