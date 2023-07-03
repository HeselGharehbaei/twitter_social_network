from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


    def clean_name(self):
        return self.cleaned_data["username"][:5]  


    def clean(self): 
        pass      
