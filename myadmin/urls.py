"""
URL configuration for Coin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from myadmin import views
urlpatterns = [
    path('dashboard/',views.AdminDashboard),
    path('users/',views.AdminUsers),
    path('search/<str:stext>/',views.AdminSearch),
    path('detail/<str:uid>/',views.AdminUserdetail),
    path('herosectionadd/',views.HeroSectionAdd),
    path('herosection/',views.HeroSection),
    path('herosectionupdate/<int:hs_id>/',views.HeroSectionUpdate),
    path('herosectiondelete/<int:hs_id>/',views.HeroSectionDelete),
    path('approve_deposit/<int:d_id>/',views.AdminApproveDeposit),
    path('approve_withdraw/<int:w_id>/',views.AdminApproveWithdraw),
    path('coin_type_list/',views.CoinTypeList),
    path('coin_type_add/',views.CoinTypeAdd),
    path('coin_type_edit/<int:ct_id>/',views.CoinTypeEdit),
    path('coin_type_delete/<int:ct_id>/',views.CoinTypeDelete),
    path('network_list/',views.NetworkList),
    path('network_add/',views.NetworkAdd),
    path('network_edit/<int:n_id>/',views.NetworkEdit),
    path('network_delete/<int:n_id>/',views.NetworkDelete),
    path('deposit_list/',views.DepositList),
    path('withdraw_list/',views.WithdrawList),
]
