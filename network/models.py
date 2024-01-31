from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    followers = models.ManyToManyField(
        "self",
        symmetrical=False, # Following someone does not mean that they also follow you
    )

class Post(models.Model):
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="Posts",
    )
    text = models.CharField(
        max_length=500,
    )
    likes = models.ManyToManyField(
        Profile,
    )
    datetime = models.DateTimeField(
        default=timezone.now
    )
