from django import forms
from .models import Post, Comment


class CreatCommentForm(forms.Form):
    text = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


    def clean_name(self):
        return self.cleaned_data["username"][:5]  


    def clean(self): 
        pass  


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text")   


class CreatCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text", ) 

