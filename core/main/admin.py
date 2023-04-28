from django.contrib import admin
from .models import PostsModel, Tag


admin.site.register(PostsModel)
admin.site.register(Tag)