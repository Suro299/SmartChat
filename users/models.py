from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    ACTIVITY_CHOICES = (
        ('all', 'all'),
        ('friends', 'friends'),
        ('nobody', 'nobody'),
    )
    
    AVATAR_CHOICES = (
        ('all', 'all'),
        ('friends', 'friends'),
    )
    
    
    # Base info
    username = models.CharField(_("User name"), max_length = 255, unique = True)
    first_name = models.CharField(_("User First Name"), max_length = 100, blank = True)
    last_name = models.CharField(_("User Last Name"), max_length = 100, blank = True)
    email = models.EmailField(_("email address"), blank = True, default = "",)
    avatar = models.ImageField(_("User avatar"), blank = True, default = "default_avatar.png",)
    description = models.TextField(_("User Description"), blank = True, default = "No BIO")
    
    # More Info
    posts_posted = models.PositiveBigIntegerField(_("posts_posted"), default = 0)
    reactions = models.PositiveBigIntegerField(_("reactions"), default = 0)
    points = models.PositiveBigIntegerField(_("points"), default = 0)
    level = models.PositiveIntegerField("User level", default = 1)
    exp = models.PositiveIntegerField("User Exp", default = 0)
    favorites = models.ManyToManyField('main.PostsModel', blank = True)
    subscribers_set = models.ManyToManyField('CustomUser', blank = True, related_name = 'subscriptions')
    subscription_set = models.ManyToManyField('CustomUser', blank = True, related_name = 'subscribers')
    friends_set = models.ManyToManyField('CustomUser', blank = True, related_name = 'friends')
    
    # other info
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    date_joined = models.DateTimeField(auto_created=True, default=timezone.now)
    
    #conf info
    avatar_visibility = models.CharField(max_length=7, choices= AVATAR_CHOICES, default='all')
    activity_visibility = models.CharField(max_length=7, choices= ACTIVITY_CHOICES, default='all')
    show_likes = models.BooleanField("Show Likes", default = False) 
    show_dislikes = models.BooleanField("Show Dislikes", default = False) 
    show_favorites = models.BooleanField("Show Favorites", default = False)



    
    
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()
    
    def update_last_login(self, user):
        user.date_joined = timezone.now()
        user.save(update_fields=['date_joined'])

    def __str__(self):
        return f"{self.username} || {self.email}"