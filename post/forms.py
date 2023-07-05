from django import forms
from .models import Post, Comment


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text")   


class CreatCommentForm(forms.ModelForm):
    created_at = forms.DateTimeField()
    class Meta:
        model = Comment
        fields = ("text","created_at") 


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "title") 
    
