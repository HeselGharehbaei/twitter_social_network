from django.shortcuts import render
from .models import Like


def home(request):
    likes = Like.objects.all()
    return render(request, 'core.html', {'Like': Like})
