from django.urls import path
from . import views

urlpatterns = [
    path("", views.posts, name = "posts"),
    path("post_page/<int:id>/", views.post_page, name = "post_page"),
    path("ftf/", views.ftf, name = "ftf"),
    path("confirm_delete/<int:id>", views.confirm_delete, name = "confirm_delete"),
    path("create_post/", views.create_post, name = "create_post"),
    path("user_more/<int:id>/<str:act>/", views.user_more, name = "user_more"),
    path("user_profile/<int:id>/", views.user_profile, name = "user_profile"),
    path("download/", views.download, name = "download"),
]

