from django.db import models
from datetime import datetime

# Create your models here.

class HeroSectionModel(models.Model):
    image = models.ImageField(default=None,null=True,blank=True)
    title = models.CharField(max_length=225)
    description = models.TextField(default=None)
    time = models.DateTimeField(default=datetime.now)

class CoinTypeModel(models.Model):
    type = models.CharField(max_length=200)
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.type

class NetworkModel(models.Model):
    type = models.CharField(max_length=200)
    qrcode = models.ImageField(default=None,null=True,blank=True)
    link_name = models.CharField(max_length=20)
    link_address = models.CharField(max_length=50)
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.type