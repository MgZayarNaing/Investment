from django.contrib import admin
from customer.models import *

# Register your models here.

admin.site.register(DepositModel)
admin.site.register(CoinModel)
admin.site.register(WithdrawModel)
