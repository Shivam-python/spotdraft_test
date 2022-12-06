from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Favourites(models.Model):
    """
    Model for storing favourite details. Added minimum fields possible
    """
    user = models.ForeignKey(User,related_name="user",on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    custom_name = models.CharField(max_length=1000,null=True,blank=True)
    obj_type = models.CharField(max_length=100,choices=[("Planets","Planets"),("Movies","Movies")])
