from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

# Create your models here.


"""class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)"""

User = get_user_model()

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures', default = 'blank-profile-picture.png')
    bio = models.TextField()
    
    def __str__self(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='post_images')
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes =  models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username



class Liked(models.Model):
    #post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.user.username
    
class Follow(models.Model):
    follower_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    #followed_user = models.CharField(max_length=250)

    def __str__(self):
        return self.follower_user.username