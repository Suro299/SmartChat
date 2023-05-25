from django.contrib import admin
from .models import ContactUs, AboutUsText, LastestUpdate

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["id", "user_username", "full_name", "date"]
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    full_name.short_description = 'Full Name'
    
    
@admin.register(AboutUsText)
class AboutUsTextModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "text"]
    search_fields = ['id', 'title', 'text']
    
@admin.register(LastestUpdate)
class LastestUpdateModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["id", "title", "text"]