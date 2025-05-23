from django.db import models
from django.contrib.auth.models import AbstractUser
from . import namekeys

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username

class Room(models.Model):
    id = models.SlugField(unique=True, blank=False, null=False, primary_key=True, max_length=50)
    edit_code = models.CharField(unique=False,null=True,max_length=250)
    description = models.TextField(unique=False,null=True,max_length=1400)
    public_list = models.BooleanField()
    passworded = models.BooleanField()
    password = models.CharField(unique=False,null=True,max_length=200)
    banned_nk = models.TextField(unique=False,null=True,blank=True,max_length=9000) #elist
    def __str__(self):
        return self.id

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    author_namekey = models.CharField(unique=False,null=True,max_length=200)
    author_ip = models.CharField(unique=False,null=True,max_length=100)
    message = models.TextField(unique=False,null=True,max_length=1400)
    room = models.ForeignKey('Room',on_delete=models.CASCADE, null=True)
    def author_name(self):
        return namekeys.decouple_nk_to_name(self.author_namekey)
    def author_nk_hash(self):
        return namekeys.hash_nk(self.author_namekey)
    def author_nk_hash_trunc(self):
        return "" + namekeys.hash_nk(self.author_namekey)[:10] + ".."
    def __str__(self):
        return f"{self.author_name()}[{self.author_nk_hash_trunc()}];#{self.id}: {self.message}"

