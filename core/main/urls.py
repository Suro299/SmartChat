from django.urls import path
from . import views

urlpatterns = [
    path("", views.posts, name = "posts"),
    path("add_post", views.add_post, name = "add_post"),
    path("login/", views.login_request, name = "login"),
    path("register/", views.register_request, name = "register"),
    path("logout/", views.logout_request, name = "logout"),
    path("del_post/<int:id>/", views.del_post, name = "del_post"),
    path("404-page/", views.ftf, name = "404-page"),
]