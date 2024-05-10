from django.shortcuts import render,redirect
from account.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from myadmin.models import *
# Create your views here.

def AdminDashboard(request):
    users = User.objects.all().order_by('-id')
    total_users = users.count()
    return render(request,"dashboard.html",{"users":users,"total_users":total_users})

def AdminUsers(request):
    users = User.objects.all().order_by('-date_joined')
    deposit = DepositModel.objects.all()
    for u in users:
        u.id = u.id.hex[:6]
    paginator = Paginator(users, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"usertables.html",{"users":page_obj,"deposit":deposit})

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
            deposit.save()
            return redirect('/myadmin/herosection/')