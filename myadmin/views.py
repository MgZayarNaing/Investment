from django.shortcuts import render
from account.models import *
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

def AdminDashboard(request):
    users = User.objects.all().order_by('-id')
    total_users = users.count()
    return render(request,"dashboard.html",{"users":users,"total_users":total_users})

def AdminUsers(request):
    users = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"usertables.html",{"users":page_obj})

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