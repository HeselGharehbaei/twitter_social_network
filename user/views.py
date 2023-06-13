from django.shortcuts import render
from .models import Account


def home(request):
    accounts = User.objects.all()
    return render(request, 'home.html', {'accounts': accounts, 'posts': posts})
