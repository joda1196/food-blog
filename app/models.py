from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(null=True, blank=True)


class BlogPost(models.Model):
    Title = models.CharField(max_length=50)
    Author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=False, auto_now_had=True)
    updated_at = models.DateField(auto_now=False, auto_now_had=True)


class Comment(models.Model):
    Author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateField(auto_now=False, auto_now_had=True)
