from django.db import models
from account import models
from myadmin.models import *


# Create your models here.

class CoinModel(models.Model):
    customer = models.ForeignKey('account.User',on_delete=models.CASCADE,default=None)
    coin_type = models.ForeignKey(CoinTypeModel,on_delete=models.CASCADE,default=None)
    network_type = models.ForeignKey(NetworkModel,on_delete=models.CASCADE,default=None)
    quantity = models.IntegerField(default=0)
    time = models.DateTimeField(default=datetime.now)

class DepositModel(models.Model):
    customer = models.ForeignKey('account.User',on_delete=models.CASCADE,default=None)
    coin_type = models.ForeignKey(CoinTypeModel,on_delete=models.CASCADE,default=None)
    network_type = models.ForeignKey(NetworkModel,on_delete=models.CASCADE,default=None)
    quantity = models.BigIntegerField(default=0)
    screenshot = models.ImageField(default=None,null=True,blank=True)
    status = models.BooleanField(default = False)
    time = models.DateTimeField(default=datetime.now)

class WithdrawModel(models.Model):
    customer = models.ForeignKey('account.User',on_delete=models.CASCADE,default=None)
    coin_type = models.ForeignKey(CoinTypeModel,on_delete=models.CASCADE,default=None)
    network_type = models.ForeignKey(NetworkModel,on_delete=models.CASCADE,default=None)
    quantity = models.BigIntegerField(default=0)
    user_link_address = models.TextField(default=None)
    status = models.BooleanField(default = False)
    time = models.DateTimeField(default=datetime.now)

class DepositHistoryModel(models.Model):
    deposit = models.ForeignKey(DepositModel,on_delete=models.CASCADE,default=None)
    time = models.DateTimeField(default=datetime.now)

class WithdrawHistoryModel(models.Model):
    withdraw = models.ForeignKey(WithdrawModel,on_delete=models.CASCADE,default=None)
    time = models.DateTimeField(default=datetime.now)