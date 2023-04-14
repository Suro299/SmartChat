from django.db import models

class PostsModel(models.Model):
    username = models.CharField("User Name", max_length = 255)
    is_staff = models.CharField("Is Staff", max_length = 10)
    
    post_title = models.CharField("Post Title", max_length = 255)
    post_text = models.TextField("Post Text")
    
    def __str__(self):
        return f"{self.username} ||  {self.post_text} || Staff: {self.is_staff}"
    
    