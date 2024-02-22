from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    followers = models.ManyToManyField(
        "self",
        symmetrical=False, # Following someone does not mean that they also follow you
        related_name='following'
    )

    def __str__(self):
        return f'{self.user.username}'

class Post(models.Model):
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    text = models.CharField(
        max_length=500,
    )
    likes = models.ManyToManyField(
        Profile,
        related_name='liked_posts',
    )
    datetime = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f'{self.owner}: {self.text}'
    
    # Custom serializer for converting into JSON
    def serialize(self):
        return {
            "owner": self.owner.user.username,
            "text": self.text,
            "likes": self.likes.count(),
            "datetime": self.datetime
        }