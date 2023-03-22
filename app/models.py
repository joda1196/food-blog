from django.db import models

# Create your models here.
class BlogPost(models.Model):
    Title = models.CharField(max_length=50)
    Author = models.CharField(max_length=50)
    created_at = models.DateField(auto_now=False, auto_now_had=True)
    updated_at = models.DateField(auto_now=False, auto_now_had=True)
