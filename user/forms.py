from django import forms
from .models import Account
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


    def clean_name(self):
        return self.cleaned_data["username"][:5]  


class UserRegistrationForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	

	def clean_email(self):
		email = self.cleaned_data['email']
		user = Account.objects.filter(email=email).exists()
		if user:
			raise ValidationError('this email already exists')
		return email
		

	def clean(self):
		cd = super().clean()
		p1 = cd.get('password1')
		p2 = cd.get('password2')

		if p1 and p2 and p1 != p2:
			raise ValidationError('password must match')


class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("username", "email", "first_name", "last_name", "phone_number", "image", "bio")  



