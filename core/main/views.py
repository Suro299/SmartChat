from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from users.models import CustomUser as User
from .forms import NewUserForm, PostModelForm
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
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect("home")
    else:
        form = PostModelForm()
        
    return render(request, 'main/add_post.html', context= {'form': form})




def register_request(request):
    pdisplay = "none"
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        pdisplay = "flex"
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
 
    return render(request, template_name='main/register.html', context= {
        "form": form,
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