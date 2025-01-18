from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username

class Room(models.Model):
    id = models.SlugField(unique=True, blank=False, null=True, max_length=50)
    owner_nk = models.CharField(unique=False,null=True,max_length=200)
    public_list = models.BooleanField()
    passworded = models.BooleanField()
    password = models.CharField(unique=False,null=True,max_length=200)
    def __str__(self):
        return self.id

class Message(models.Model):
    author_nk = models.CharField(unique=False,null=True,max_length=200)
    author_ip = models.CharField(unique=False,null=True,max_length=80)
    message = models.TextField(unique=False,null=True,max_length=1400)
    room = models.ForeignKey('Room',on_delete=models.CASCADE, null=True)
