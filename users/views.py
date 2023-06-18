from django.shortcuts import render, redirect
from .forms import NewUserForm
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
from .models import CustomUser as User

def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        username = request.POST.get("username")
        user_email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        
        if username in User.objects.values_list('username', flat=True):
            return render(request, "users/register.html", {
                "form": form,
                "message": "Username already taken"
            })
        
        
        if password1 != password2:
            return render(request, "users/register.html", {
                "form": form,
                "message": "Password mismatch"
                })
            
        if len(password1) < 6:
            return render(request, "users/register.html", {
                "form": form,
                "message": "Minimum password length 6 characters"
            })

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activation link has been sent to your email id"
            message = render_to_string(
                "users/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")

            email = EmailMessage(
                mail_subject,
                message,
                to=[to_email],
                from_email="SmartChat <your_email@example.com>",
            )

            email.content_subtype = "html"
            email.send()

            return render(
                request, "users/pls_check_email.html", context={
                    "user_email": user_email,
                    }
            )
    else:
        form = NewUserForm()

    return render(request, "users/register.html", {
        "form": form,
        "message": ""
        })


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "users/verif_email.html")
    else:
        return render(request, "users/invalid_link.html")


def login_request(request):
    message = ''
    if request.user.is_authenticated:
        return redirect("posts")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("posts")
            else:
                messages.error(request, "Invalid username or password.")
                
        else:
            messages.error(request, "Invalid username or password.")
            username = form.cleaned_data.get("username")
            if username in  User.objects.values_list('username', flat=True) and username != "":
                message = "Invalid Password"
            else:
                message = "User is not found"
            
    form = AuthenticationForm()
    
    return render(
        request=request, template_name="users/login.html", context={
            "login_form": form, 
            "message": message
        }
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("posts")


def verif_email(request):
    return render(request, "users/verif_email.html")


def pls_check_email(request):
    return render(request, "users/pls_check_email.html")


def invalid_link(request):
    return render(request, "users/invalid_link.html")
