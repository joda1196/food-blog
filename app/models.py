from django.db import models
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class BlogPost(models.Model):
    Title = models.CharField(max_length=50)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=False)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.author.user.username + ' | ' + self.Title


class Comment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=False)
    created_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.author.user.username + ': '  + self.created_on.__str__()
