from django.shortcuts import render

from .models import Film
from .films import get_films


def sponsor(request):
    get_films()
    
    
    films = Film.objects.all()
    return render(request, "sponsor/sponsor.html", context = {
        "films": films
    })

