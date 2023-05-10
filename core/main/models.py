from django.db import models
from users.models import CustomUser
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField("Tag Name", max_length = 30)
    def __str__(self) -> str:
        return self.name



class PostsModel(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    post_title = models.CharField("Post Title", max_length = 255)
    post_text = models.TextField("Post Content")
    post_image = models.ImageField("Post Image", blank = True)
    post_tags = models.CharField("Post Title", max_length = 100, blank = True)
    comments = models.PositiveBigIntegerField("Comments Count", blank = True, default = 0)
    timestamp = models.DateTimeField(auto_now_add = True)

    post_tags = models.ManyToManyField("Tag", blank = True)
    likers = models.ManyToManyField(CustomUser, related_name = "likers", blank = True)
    dislikers = models.ManyToManyField(CustomUser, related_name = "dislikers", blank = True)
    date_created = models.DateTimeField("Data Created", auto_created = True, default = timezone.now)

    
    def __str__(self) -> str:
        return f"{self.post_title}"

