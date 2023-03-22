from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
<<<<<<< HEAD
class BlogPost(models.Model):
    Title = models.CharField(max_length=50)
    Author = models.CharField(max_length=50)
    created_at = models.DateField(auto_now=False, auto_now_had=True)
    updated_at = models.DateField(auto_now=False, auto_now_had=True)
=======
class Profile(models.Model):
    name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(null=True, blank=True)

>>>>>>> 46bbd363afed3fcb63e6cb9f04c0f5b76126c665
