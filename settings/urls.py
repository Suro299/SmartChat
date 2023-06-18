from django.urls import path
from . import views

urlpatterns = [
    path("", views.profil_settings, name = "profil_settings"),
    path("confidentiality/", views.confid_settings, name = "confid_settings"),
]

