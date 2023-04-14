from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("add_post", views.add_post, name = "add_post"),
    path("login/", views.login_request, name = "login"),
    path("register/", views.register_request, name = "register"),
    path("logout/", views.logout_request, name = "logout")
]