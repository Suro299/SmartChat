from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from users.models import CustomUser as User
from .forms import NewUserForm, PostModelForm
from .models import PostsModel


def home(request):
    if not(request.user.is_authenticated): 
        return redirect("login")

    user_list = User.objects.all()
    post_list = PostsModel.objects.all()[::-1]

    if request.method == "POST":
        
        btn_l = request.POST.get("btn_l")    
        btn_d = request.POST.get("btn_d") 
        
        if btn_l:
            prod = PostsModel.objects.get(id = btn_l)
            post = PostsModel.objects.get(id= btn_l)
            if request.user in prod.likers.all():
                prod.like -= 1
                post.likers.remove(request.user)
                
            else:
                prod.like += 1
                post.likers.add(request.user)
                
                if request.user in prod.dislikers.all():
                    prod.dislike -= 1
                    post.dislikers.remove(request.user)
                    
                    
        elif btn_d:    
            prod = PostsModel.objects.get(id = btn_d)
            post = PostsModel.objects.get(id= btn_d)
            
            if request.user in prod.dislikers.all():
                prod.dislike -= 1
                post.dislikers.remove(request.user)
                
            else:
                prod.dislike += 1
                post.dislikers.add(request.user)
                
                if request.user in prod.likers.all():
                    prod.like -= 1
                    post.likers.remove(request.user)
                    
            
        prod.save()  
        
        
       
         
        return redirect("home")

    return render(request, "main/home.html", context = {
            "user_list": user_list,
            "post_list": post_list,
        })

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