from django.db import models
from django.utils import timezone
from users.models import CustomUser as User
from django.utils import timezone


class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    message = models.TextField("Message")
    date = models.DateTimeField(auto_created=True, default=timezone.now)
    
    
    class Meta:
        verbose_name = "Contact Us Message"
        verbose_name_plural = "Contact Us Messages"
    
    def __str__(self) -> str:
        return f"{self.user.username}"



class AboutUsText(models.Model):
    title = models.CharField("Title", max_length = 255)
    text = models.TextField("Text")
    
     
    class Meta:
        verbose_name = "About Us Text"
        verbose_name_plural = "About Us Text"
    
    def __str__(self) -> str:
        return f"{self.title } | {self.text[:10]}"



class LastestUpdate(models.Model):
    title = models.CharField("Update Title", max_length = 255)
    text = models.TextField("Update Text")
    date = models.DateTimeField(auto_created=True, default=timezone.now)
    
    class Meta:
        verbose_name = "Lastest Update"
        verbose_name_plural = "Lastest Updates"
        
    def __str__(self) -> str:
        return f"{self.title} || {self.date}"