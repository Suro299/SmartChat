from django.shortcuts import render, redirect


def login(request):
    return render(request, "main/login.html")

def register(request):
    return render(request, "main/register.html")

def home(request):
    if request.user.is_authenticated: 
        return render(request, "main/home.html")
    else: 
        return render(request, "main/login.html")
    
