from django.db import models
from django.utils import timezone
from users.models import CustomUser as User


class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    message = models.TextField("Message")
    date = models.DateTimeField(auto_created=True, default=timezone.now)
    
    
    class Meta:
        verbose_name = "Contact Us Message"
        verbose_name_plural = "Contact Us Messages"
    
    def __str__(self) -> str:
        return f"{self.user.username}"


