from django.shortcuts import render,redirect
from account.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from myadmin.models import *
from customer.models import *
# Create your views here.

def CoinTypeAdd(request):
    if request.method == "GET":
        return render(request,"coin_type_add.html")
    if request.method == "POST":
        coin_type = CoinTypeModel.objects.create(
            type = request.POST.get('type'),
            time = datetime.now()
        )
        coin_type.save()
        return redirect('/myadmin/coin_type_list/')

def CoinTypeList(request):
    coin_type = CoinTypeModel.objects.all().order_by('-time')
    return render(request,"coin_type_list.html",{"coin_type":coin_type})

def CoinTypeEdit(request,ct_id):
    if request.method == "GET":
        coin_type = CoinTypeModel.objects.get(id = ct_id)
        return render(request,"coin_type_edit.html",{"coin_type":coin_type})
    if request.method == "POST":
        coin_type = CoinTypeModel.objects.get(id = ct_id)
        coin_type.type = request.POST.get('type')
        coin_type.save()
        return redirect('/myadmin/coin_type_list/')
    
def CoinTypeDelete(request,ct_id):
    coin_type = CoinTypeModel.objects.get(id = ct_id)
    coin_type.delete()
    return redirect('/myadmin/coin_type_list/')

def NetworkAdd(request):
    if request.method == "GET":
        return render(request,"network_add.html")
    if request.method == "POST":
        network = NetworkModel.objects.create(
            type = request.POST.get('type'),
            qrcode = request.FILES.get('qrcode'),
            link_name = request.POST.get('link_name'),
            link_address = request.POST.get('link_address'),
            time = datetime.now()
        )
        network.save()
        return redirect('/myadmin/network_list/')

def NetworkList(request):
    network = NetworkModel.objects.all().order_by('-time')
    return render(request,"network_list.html",{"network":network})

def NetworkEdit(request,n_id):
    if request.method == "GET":
        network = NetworkModel.objects.get(id = n_id)
        return render(request,"network_edit.html",{"network":network})
    if request.method == "POST":
        network = NetworkModel.objects.get(id = n_id)
        network.type = request.POST.get('type')
        if request.FILES.get('qrcode'):
            network.qrcode.delete()
            network.qrcode = request.FILES.get('qrcode')
        network.link_name = request.POST.get('link_name')
        network.link_address = request.POST.get('link_address')
        network.save()
        return redirect('/myadmin/network_list/')
    
def NetworkDelete(request,n_id):
    network = NetworkModel.objects.get(id = n_id)
    if request.FILES.get('qrcode'):
        network.qrcode.delete()
    network.delete()
    return redirect('/myadmin/network_list/')

def AdminDashboard(request):
    users = User.objects.all().order_by('-id')
    total_users = users.count()
    return render(request,"dashboard.html",{"users":users,"total_users":total_users})

def AdminUsers(request):
    users = User.objects.all().order_by('-date_joined')
    deposit = DepositModel.objects.all()
    withdraw = WithdrawModel.objects.all()
    for u in users:
        u.id = u.id.hex[:6]
    paginator = Paginator(users, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"usertables.html",{"users":page_obj,"deposit":deposit,"withdraw":withdraw})

def AdminUserdetail(request,uid):
    user = User.objects.get(id=uid)
    return render(request,"user_detail.html",{"user":user})

def AdminSearch(request,stext):
        users = User.objects.filter(
            Q(name__icontains=stext) |
            Q(email__icontains=stext)
            )
        paginator = Paginator(users, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,"usertables.html",{"users":page_obj})

def HeroSectionAdd(request):
     if request.method == "GET":
          return render(request,"HeroSectionAdd.html")
     if request.method == "POST":
          herosection = HeroSectionModel.objects.create(
               title = request.POST.get('title'),
               image = request.FILES.get('image'),
               description = request.POST.get('description'),
               time = datetime.now()
          )
          herosection.save()
          return redirect('/myadmin/herosection/')
     
def HeroSection(request):
    herosection = HeroSectionModel.objects.all().order_by('-time')[:1]
    return render(request,"HeroSection.html",{"herosection":herosection})

def HeroSectionUpdate(request,hs_id):
     herosection = HeroSectionModel.objects.get(id = hs_id)
     if request.method == "GET":
          return render(request,"HeroSectionUpdate.html",{"herosection":herosection})
     if request.method == "POST":
          herosection.title = request.POST.get('title')
          if request.FILES.get('image'):
                herosection.image.delete()
                herosection.image = request.FILES.get('image')
          herosection.description = request.POST.get('description')
          herosection.save()
          return redirect('/myadmin/herosection/')
     
def HeroSectionDelete(request,hs_id):
    herosection = HeroSectionModel.objects.get(id = hs_id)
    if request.FILES.get('image'):
        herosection.image.delete()
    herosection.delete()
    return redirect('/myadmin/herosection/')

def DepositList(request):
    deposit = DepositModel.objects.all().order_by('-time')
    deposit_history = DepositHistoryModel.objects.all().order_by('-time')
    return render(request,'deposit_list.html',{"deposit":deposit,"deposit_history":deposit_history})

def DepositHistory(request):
    deposit_history = DepositHistoryModel.objects.all()
    return render(request,"deposit_history.html",{"deposit_history":deposit_history})

def WithdrawHistory(request):
    withdraw_history = WithdrawHistoryModel.objects.all()
    return render(request,"withdraw_history.html",{"withdraw_history":withdraw_history})

def WithdrawList(request):
    withdraw = WithdrawModel.objects.all().order_by('-time')
    withdraw_history = WithdrawHistoryModel.objects.all().order_by('-time')
    return render(request,'withdraw_list.html',{"withdraw":withdraw,"withdraw_history":withdraw_history})

def AdminApproveDeposit(request,d_id):
    if request.method == "POST":
        deposit = DepositModel.objects.get(id = d_id)
        deposit.status = True

        have_deposit = CoinModel.objects.filter(customer_id = deposit.customer.id)
        if have_deposit:
            coin = CoinModel.objects.get(customer_id = deposit.customer.id) 
            coin.network_type_id = deposit.network_type
            coin.coin_type_id = deposit.coin_type 
            coin.quantity += deposit.quantity
            coin.save()

            deposit_history = DepositHistoryModel.objects.create(
                deposit_id = d_id,
                time = datetime.now()
            )
            deposit_history.save()
            deposit.save()
            
            
            return redirect('/myadmin/herosection/')
        else:
            coin = CoinModel.objects.create(
                customer_id = deposit.customer.id,
                network_type_id = deposit.network_type_id,
                coin_type_id = deposit.coin_type_id,
                quantity = deposit.quantity,
                time = datetime.now()
            )
            coin.save()
            deposit_history = DepositHistoryModel.objects.create(
                deposit_id = d_id,
                time = datetime.now()
            )
            deposit_history.save()
            deposit.save()
            return redirect('/myadmin/herosection/')
        
def AdminApproveWithdraw(request,w_id):
    if request.method == "POST":
        withdraw = WithdrawModel.objects.get(id = w_id)
        withdraw.status = True

        have_withdraw = CoinModel.objects.filter(customer_id = withdraw.customer.id)
        if have_withdraw:
            coin = CoinModel.objects.get(customer_id = withdraw.customer.id) 
            coin.network_type_id = withdraw.network_type
            coin.coin_type_id = withdraw.coin_type 
            coin.quantity -= withdraw.quantity
            coin.save()

            withdraw_history = WithdrawHistoryModel.objects.create(
                withdraw_id = w_id,
                time = datetime.now()
            )
            withdraw_history.save()
            withdraw.save()
            
            
            return redirect('/myadmin/herosection/')
        else:
            coin = CoinModel.objects.create(
                customer_id = withdraw.customer.id,
                network_type_id = withdraw.network_type_id,
                coin_type_id = withdraw.coin_type_id,
                quantity = withdraw.quantity,
                time = datetime.now()
            )
            coin.save()
            withdraw_history = DepositHistoryModel.objects.create(
                withdraw_id = w_id,
                time = datetime.now()
            )
            withdraw_history.save()
            withdraw.save()
            return redirect('/myadmin/herosection/')