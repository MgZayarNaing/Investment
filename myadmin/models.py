from django.db import models
from datetime import datetime

# Create your models here.

class HeroSectionModel(models.Model):
    image = models.ImageField(default=None,null=True,blank=True)
    title = models.CharField(max_length=225)
    description = models.TextField(default=None)
    time = models.DateTimeField(default=datetime.now)