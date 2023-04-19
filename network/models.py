from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    body = models.CharField(max_length=640)                                         # Post text
    date = models.DateTimeField(auto_now_add=True)                                  # Creation date
    date_edit = models.DateTimeField(auto_now=True, blank=True)                     # Edit date
    user = models.ForeignKey(User, on_delete=models.CASCADE)                        # User
    likes = models.ManyToManyField(User, blank=True, related_name="users_likes")    # Likes


    def __str__(self):
        return str(self.user) + "_" + str(self.id)

    
