from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'orderScreen.html')

def swipe(request):
    return render(request, 'orderScreenSwipe.html')