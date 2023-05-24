from django.shortcuts import render, redirect

from .models import ContactUs
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