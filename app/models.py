from django.db import models
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    Title = models.CharField(max_length=50)
    post_author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    content = models.TextField(null=True, blank=False)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.post_author


class Comment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.PROTECT)
    comment_author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    content = models.TextField(null=True, blank=False)
    created_on = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.comment_author
