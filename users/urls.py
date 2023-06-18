from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_request, name = "login"),
    path("register/", views.signup, name = "register"),
    path("pls_check_email/", views.pls_check_email, name = "pls_check_email"),
    path("verif_email/", views.verif_email, name = "verif_email"),
    path("invalid_link/", views.invalid_link, name = "invalid_link"),
    path('logout/', views.logout_request, name='logout'),
    path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  views.activate, name='activate'),  
]

