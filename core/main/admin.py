from django.contrib import admin
from .models import Tag, PostsModel, Comment
from django.db.models import Q


@admin.register(Tag)
class TagaModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]



@admin.register(PostsModel)
class PostsModelAdmin(admin.ModelAdmin):
    list_display = ["id", "sender_username", "sender_full_name", "likers_count",
                    "dislikers_count", "comments_count", "date_created",
                    ]
    
    search_fields = ["id", "sender__username", "sender__first_name",
                     "sender__last_name", "comments__id", "comments__text",
                    ]

    def sender_username(self, obj):
        return obj.sender.username
    sender_username.short_description = "Sender Username"

    def sender_full_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"
    sender_full_name.short_description = "Sender Full Name"

    def likers_count(self, obj):
        return obj.likers.count()
    likers_count.short_description = "Likers Count"

    def dislikers_count(self, obj):
        return obj.dislikers.count()
    dislikers_count.short_description = "Dislikers Count"
    
    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = "Comments Count"

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(
                Q(comments__id__icontains=search_term) |
                Q(comments__text__icontains=search_term)
            )
        return queryset, use_distinct

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "sender_full_name", "date_created"]
    search_fields = ["sender__username", "sender__first_name", "sender__last_name"]

    def sender(self, obj):
        return obj.com_sender.username
    sender.short_description = "Sender Username"

    def sender_full_name(self, obj):
        return f"{obj.com_sender.first_name} {obj.com_sender.last_name}"
    sender_full_name.short_description = " Sender Full Name"
