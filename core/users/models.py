from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("User name"), max_length=255, unique=True)
    email = models.EmailField(_("email address"), blank=True, default="",)
    avatar = models.ImageField(_("User avatar"), blank=True, default="default_avatar.png",)
    description = models.TextField(_("User Description"), blank = True, default = "No BIO")
    posts_posted = models.PositiveBigIntegerField(_("posts_posted"), default=0)
    reactions = models.PositiveBigIntegerField(_("reactions"), default=0)
    points = models.PositiveBigIntegerField(_("points"), default=0)
    level = models.PositiveIntegerField("User level", default=1)
    exp = models.PositiveIntegerField("User Exp", default=0)
    favorites = models.ManyToManyField('main.PostsModel', blank = True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    subscribers_set = models.ManyToManyField('CustomUser', blank=True, related_name='subscriptions')
    subscription_set = models.ManyToManyField('CustomUser', blank=True, related_name='subscribers')
    friends_set = models.ManyToManyField('CustomUser', blank=True, related_name='friends')
    
    date_joined = models.DateTimeField(auto_created=True, default=timezone.now)
    
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} || {self.email}"