from django.shortcuts import render,redirect
from myadmin.models import *
import telepot
from account.models import *
from customer.models import *
from django.http import JsonResponse

# Create your views here.

def HomePage(request):
    herosection = HeroSectionModel.objects.all().order_by('-time')[:1]
    token = '6779452535:AAFyEG35dthKQJpZz9kOj2RTg46QwbXoukg'    
    receiver_id = -1002045674406
    bot = telepot.Bot(token)
    bot.sendMessage(receiver_id, f'New login user')

    return render(request,'home.html',{"herosection":herosection})

def Withdraw(request):
    return render(request,'withdraw.html')

def Deposit(request):
    if request.method == "GET":
        coin_type = CoinTypeModel.objects.all()
        network = NetworkModel.objects.all()
        return render(request, 'deposit.html', {"coin_type": coin_type, "network": network})

    if request.method == "POST":
        deposit = DepositModel.objects.create(
            customer_id = request.user.id,
            coin_type_id=request.POST.get('coin_type'),
            network_type_id=request.POST.get('network'),
            quantity=request.POST.get('quantity'),
            screenshot=request.FILES.get('screenshot'),
            time=datetime.now(),
        )
        
        return redirect('/')
    
    
def GetQRLink(request):
    option_id = request.GET.get('option_id')
    option = NetworkModel.objects.get(pk=option_id)
    image_url = option.qrcode.url
    return JsonResponse({'image_url': image_url,'link_name': option.link_name,'link_address':option.link_address})

def Account(request):
    user = User.objects.get(id = request.user.id)
    user.id = user.id.hex[:6]
    try:
        coin = CoinModel.objects.get(customer_id = request.user.id)
    except Exception as e:
        coin = None
    return render(request,'account.html',{"user":user,"coin":coin})


