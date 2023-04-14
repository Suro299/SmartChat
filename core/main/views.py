from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import RegistrationForm, PostModelForm
from .models import PostsModel


def home(request):
    user_list = User.objects.all()
    post_list = PostsModel.objects.all()[::-1]
    if request.user.is_authenticated: 
        return render(request, "main/home.html", context = {
            "user_list": user_list,
            "post_list": post_list
        })
    else: 
        return redirect("login")

def add_post(request):
    if request.method == "POST":
        form = PostModelForm(request.POST)
        
        if form.is_valid():
            PostsModel.objects.create(**form.cleaned_data)
            return redirect("home")
    else:
        form = PostModelForm()
        
    return render(request, "main/add_post.html", context = {
        "form": form
    })

def register_request(request):
    pdisplay = "none"
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():  
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            User.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
        pdisplay = "flex"
    else:
        form = RegistrationForm()
        
    return render(request, template_name='main/register.html', context= {
        'form': form,
        "pdisplay": pdisplay
        })





def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
           username = form.cleaned_data.get('username')
           password = form.cleaned_data.get('password')
           user = authenticate(username=username, password=password)
           if user is not None:
               login(request, user)
               messages.info(request, f"You are now logged in as {username}.")
               return redirect("home")
           else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    print("aa")
    
    return render(request=request, template_name="main/login.html", context={"login_form":form})



def logout_request(request):

	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")