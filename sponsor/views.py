from django.shortcuts import render, redirect

from .models import Film
from .films import get_films
from main.views import get_unread_messages_count

def sponsor(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    unread_msg = get_unread_messages_count(request) 
       
    get_films()
    
    films = Film.objects.all()[::-1]
    return render(request, "sponsor/sponsor.html", context = {
        "films": films,
        "total_unread_messages": unread_msg,
    })

