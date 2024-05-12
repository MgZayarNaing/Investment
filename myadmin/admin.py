from django.contrib import admin
from myadmin import models
from customer import models
# Register your models here.

admin.site.register(models.HeroSectionModel)
admin.site.register(models.CoinTypeModel)
admin.site.register(models.NetworkModel)
admin.site.register(models.DepositHistoryModel)
admin.site.register(models.WithdrawHistoryModel)


