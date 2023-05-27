from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_request, name = "login"),
    path("register/", views.signup, name = "register"),
    path("posts/", views.posts, name = "posts"),
    path("post_page/<int:id>/", views.post_page, name = "post_page"),
    path("ftf/", views.ftf, name = "ftf"),
    path("confirm_delete/<int:id>", views.confirm_delete, name = "confirm_delete"),
    path("create_post/", views.create_post, name = "create_post"),
    path("confid_settings/", views.confid_settings, name = "confid_settings"),
    path("profil_settings/", views.profil_settings, name = "profil_settings"),
    path("user_more/<str:act>", views.user_more, name = "user_more"),
    path("user_profile/<int:id>/", views.user_profile, name = "user_profile"),
    path("pls_check_email/", views.pls_check_email, name = "pls_check_email"),
    path("verif_email/", views.verif_email, name = "verif_email"),
    path("invalid_link/", views.invalid_link, name = "invalid_link"),
    path('logout/', views.logout_request, name='logout'),
    path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  views.activate, name='activate'),  
]

