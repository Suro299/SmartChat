from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from .forms import NewUserForm
from users.models import CustomUser as User



def posts(reuqest):
    return render(reuqest, "main/posts.html")


def about_us(reuqest):
    return render(reuqest, "main/about_us.html")

def contact_us(reuqest):
    return render(reuqest, "main/contact_us.html")




def confid_settings(reuqest):
    return render(reuqest, "main/confid_settings.html")


def confirm_delete(reuqest):
    return render(reuqest, "main/confirm_delete.html")



def create_post(reuqest):
    return render(reuqest, "main/create_post.html")




def lastest_update(reuqest):
    return render(reuqest, "main/lastest_update.html")





def post_page(reuqest):
    return render(reuqest, "main/post_page.html")


def profil_settings(reuqest):
    return render(reuqest, "main/profil_settings.html")





def signup(request):  
    if request.method == 'POST':  
        form = NewUserForm(request.POST)  
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
            return render(request, "main/pls_check_email.html")
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





def user_more(reuqest):
    return render(reuqest, "main/user_more.html")


def user_profile(reuqest):
    return render(reuqest, "main/user_profile.html")






def verif_email(reuqest):
    return render(reuqest, "main/verif_email.html")

def pls_check_email(reuqest):
    return render(reuqest, "main/pls_check_email.html")

def invalid_link(reuqest):
    return render(reuqest, "main/invalid_link.html")



def ftf(reuqest):
    return render(reuqest, "main/404.html")

