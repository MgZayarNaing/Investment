from django.shortcuts import render
from myadmin.models import *
import telepot

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

def Account(request):
    return render(request,'account.html')


