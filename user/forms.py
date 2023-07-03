from django import forms
from .models import Account


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


    def clean_name(self):
        return self.cleaned_data["username"][:5]  


    def clean(self): 
        pass   


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("username", "email", "password", "phone_number")