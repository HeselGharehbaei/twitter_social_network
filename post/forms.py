from django import forms
from .models import Post, Comment, Image, Tag  


class CreatCommentForm(forms.ModelForm):
    created_at = forms.DateTimeField()
    class Meta:
        model = Comment
        fields = ("text","created_at") 


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text") 


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("name", "image", "alt") 


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name", ) 




    
