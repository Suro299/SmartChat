from django.shortcuts import render, redirect

from users.models import CustomUser as User

from main.models import PostsModel

from .models import ContactUs, AboutUsText, LastestUpdate
from .forms import NewMessage


def contact_us(request):
    if not (request.user.is_authenticated):
        return redirect("/")
    
    if request.method == "POST":
        form = NewMessage(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            ContactUs.objects.create(user = request.user, message = form.cleaned_data["message"])
            return redirect("/posts")
    else:
        form = NewMessage()
    
    return render(request, "about_us/contact_us.html", context = {
        "form": form
    })
    
def about_us(request):
    if not (request.user.is_authenticated):
        return redirect("/")
    
    about_us = AboutUsText.objects.all()[0]
    about_us_text = str(about_us.text).split("\n")
    about_us_title = about_us.title

    users_count = User.objects.all().count()
    posts_count = PostsModel.objects.all().count()
    
    return render(request, "about_us/about_us.html", context = {
        "users_count": users_count,
        "posts_count": posts_count,
        "about_us_title": about_us_title,
        "about_us_text": about_us_text
    })



def lastest_update(request):
    if not (request.user.is_authenticated):
        return redirect("/")
    
    
    lastest_update = LastestUpdate.objects.all()[::-1]
    
    return render(request, "about_us/lastest_update.html", context = {
        "lastest_update": lastest_update
    })
