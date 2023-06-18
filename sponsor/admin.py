from django.contrib import admin
from .models import Film


@admin.register(Film)
class FilmAdminModel(admin.ModelAdmin):
    list_display = ["id", "title", "genre", "year"]
    search_fields = ["id", "title", "genre", "year"]
    