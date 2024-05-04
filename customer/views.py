from django.shortcuts import render
from myadmin.models import *

# Create your views here.

def HomePage(request):
    herosection = HeroSectionModel.objects.all().order_by('-time')[:1]
    return render(request,'home.html',{"herosection":herosection})
