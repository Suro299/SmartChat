from django.db import models
from users.models import CustomUser
 
    
class PostsModel(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    post_title = models.CharField("Post Title", max_length = 255)
    post_text = models.TextField("Post Content")
    post_image = models.ImageField("Post Image")
    like = models.PositiveBigIntegerField("Likes Count", blank = True, default = 0)
    dislike = models.PositiveBigIntegerField("Dislikes Count", blank = True, default = 0)
    comments = models.PositiveBigIntegerField("Comments Count", blank = True, default = 0)
    timestamp = models.DateTimeField(auto_now_add = True)
    
    likers = models.ManyToManyField(CustomUser, related_name = "likers", blank = True)
    dislikers = models.ManyToManyField(CustomUser, related_name = "dislikers", blank = True)
    
    def __str__(self) -> str:
        return f"{self.post_title}"
    
