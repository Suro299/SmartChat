from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from users.models import CustomUser as User
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from .forms import NewUserForm, NewPostModelForm, NewComment
from .models import PostsModel, Tag, Comment



def posts(request):
    if not(request.user.is_authenticated):
        return redirect("login")
    
    
    if request.method == "POST":

        btn_l = request.POST.get("btn_l")    
        btn_d = request.POST.get("btn_d") 
        btn_f = request.POST.get("btn_f") 
        
        user = User.objects.get(username = request.user.username)
        
      
        if btn_l:
            prod = PostsModel.objects.get(id = btn_l)
            
            if request.user in prod.likers.all():
                prod.likers.remove(request.user)
            else:
                prod.likers.add(request.user)
                if request.user in prod.dislikers.all():
                    prod.dislikers.remove(request.user)
                    
        elif btn_d:    
            prod = PostsModel.objects.get(id = btn_d)
            
            if request.user in prod.dislikers.all():
                prod.dislikers.remove(request.user)
            else:
                prod.dislikers.add(request.user)
                
                if request.user in prod.likers.all():
                    prod.likers.remove(request.user)
        
        elif btn_f:
            prod = PostsModel.objects.get(id = btn_f)
            
            if prod in user.favorites.all():
                user.favorites.remove(prod)
            else:
                user.favorites.add(prod)
        
        try:
            prod.save()  
            user.save()
        except:
            pass
        
    posts_list = PostsModel.objects.all()[::-1]
    return render(request, "main/posts.html", context = {
        "posts_list": posts_list,
    })
    


def about_us(request):
    return render(request, "main/about_us.html")

def contact_us(request):
    return render(request, "main/contact_us.html")




def confid_settings(request):
    return render(request, "main/confid_settings.html")


def confirm_delete(request):
    return render(request, "main/confirm_delete.html")



def create_post(request):
    
    if request.method == "POST":
        
        post_tags = request.POST.get("post_tags")

        form = NewPostModelForm(request.POST, request.FILES)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            
            if post_tags:
                tags = post_tags.split(" ")

                for i in tags:
                    i = i.strip()

                    if i != "" and i != "#" and i[0] == "#":
                        tag_instance, _ = Tag.objects.get_or_create(name = i[1:])
                        message.post_tags.add(tag_instance) 
            
            user = User.objects.get(username=request.user.username)
            user.posts_posted += 1
            user.exp += 4
    
            if user.exp >= 100:
                user.exp -= 100
                user.level += 1

            user.save()

            return redirect("posts")
        else:
            print("!!! Post Creation Validation !!! ")
    else:
        form = NewPostModelForm()
    
    return render(request, "main/create_post.html", context = {
        "form": form
    })




def lastest_update(request):
    return render(request, "main/lastest_update.html")





def post_page(request, id):
    print(id)
    post = PostsModel.objects.get(pk = id)
    
    if request.method == "POST":
        btn_l = request.POST.get("btn_l")    
        btn_d = request.POST.get("btn_d") 
        post_comment = request.POST.get("post_comment") 
        print(btn_l, btn_d, post_comment)
        if btn_l:
            comment_ex = Comment.objects.get(id = btn_l)
            
            if request.user in comment_ex.likers.all():
                comment_ex.likers.remove(request.user)
            else:
                comment_ex.likers.add(request.user)
                if request.user in comment_ex.dislikers.all():
                    comment_ex.dislikers.remove(request.user)
                    
        elif btn_d:    
            comment_ex = Comment.objects.get(id = btn_d)
            
            if request.user in comment_ex.dislikers.all():
                comment_ex.dislikers.remove(request.user)
            else:
                comment_ex.dislikers.add(request.user)
                
                if request.user in comment_ex.likers.all():
                    comment_ex.likers.remove(request.user)
        
        elif post_comment:
            form = NewComment(request.POST)
            
            if form.is_valid():
                comment = form.save(commit=False)
                comment.com_sender = request.user
                comment.save()
                post.comments.add(comment)
                
    else:
        form = NewComment()
    
    return render(request, "main/post_page.html", context = {
        "post": post
    })





def profil_settings(request):
    return render(request, "main/profil_settings.html")





# def signup(request):  
    if request.method == 'POST':  
        form = NewUserForm(request.POST)  
        user_email = request.POST.get("email")
        
        if form.is_valid():  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('main/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            
            email = EmailMessage(  
                    mail_subject, message, to=[to_email]  
            ) 
             
            email.send()  
            return render(request, "main/pls_check_email.html", context = {
                "user_email": user_email
            })
    else:  
        form = NewUserForm()  
    return render(request, 'main/register.html', {'form': form})  


def signup(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        user_email = request.POST.get("email")

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('main/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')

            email = EmailMessage(
                mail_subject,
                message,
                to=[to_email],
                from_email='SmartChat <your_email@example.com>', # указываете имя и email отправителя
            )
            
            email.content_subtype = 'html'
            email.send()

            return render(request, "main/pls_check_email.html", context={"user_email": user_email})
    else:
        form = NewUserForm()

    return render(request, 'main/register.html', {'form': form})


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return render(request, "main/verif_email.html") 
    else:  
        return render(request, "main/invalid_link.html")  


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
				return redirect("posts")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("posts")





def user_more(request):
    return render(request, "main/user_more.html")


def user_profile(request):
    return render(request, "main/user_profile.html")






def verif_email(request):
    return render(request, "main/verif_email.html")

def pls_check_email(request):
    return render(request, "main/pls_check_email.html")

def invalid_link(request):
    return render(request, "main/invalid_link.html")



def ftf(request):
    return render(request, "main/404.html")

