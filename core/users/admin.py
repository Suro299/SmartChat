from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username", "email", "level", "exp", "is_staff", "is_active", "avatar")
    list_filter = ("username", "email", "level", "exp","is_staff", "is_active", "subscribers_set", "subscription_set", "friends_set")
    
    fieldsets = (
        ("Basic Information", {"fields": ("username", "first_name", "last_name", "email", "description", "avatar")}),
        ("More Info", {"fields": ("date_joined", "level", "exp", "posts_posted", "reactions", "points", "favorites", "subscribers_set","subscription_set", "friends_set")}),
        ("Confidentiality Info", {"fields": ("activity_visibility", "avatar_visibility", "show_likes", "show_dislikes", "show_favorites")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    

    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions", "avatar", "level", "exp", 'favorites', "subscription_set"
            )}
        ),
    )
    search_fields = ("email", "username")
    ordering = ("username", "is_staff")


admin.site.register(CustomUser, CustomUserAdmin)
