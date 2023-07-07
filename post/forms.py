from django import forms
from .models import Post, Comment, Image, Tag  


class CreatCommentForm(forms.ModelForm):
    created_at = forms.DateTimeField()
    class Meta:
        model = Comment
        fields = ("text","created_at") 


class PostForm(forms.ModelForm):
    is_archived = forms.BooleanField(required=False, )
    class Meta:
        model = Post
        fields = ("title", "text", "is_archived") 


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("name", "image", "alt") 
        labels = {
            'name': 'image name',
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name", ) 
        labels = {
            'name': 'tag name',
        }




    
