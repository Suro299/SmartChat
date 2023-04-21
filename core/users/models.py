from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("User name"), max_length=255, unique=True)
    email = models.EmailField(_("email address"), blank=True, default = "",)
    avatar = models.ImageField(_("User avatar"), blank=True, default = "default_avatar.png",)
    posts_posted = models.PositiveBigIntegerField(_("posts_posted"), blank = True, default = 0)
    reactions = models.PositiveBigIntegerField(_("reactions"), blank = True, default = 0)
    points = models.PositiveBigIntegerField(_("points"), blank = True, default = 0)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} || {self.email}"