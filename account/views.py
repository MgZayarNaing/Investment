from django.shortcuts import render,redirect
from account.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import check_password
from datetime import datetime

# Create your views here.

def LogIn(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=username)
            if check_password(password, user.password):
                login(request, user)
                messages.success(request, "You are now logged in as "+ username)
                return redirect('/chat-admin/')
            else:
                messages.error(request, " Password is incorrect!")
                return render(request, 'login.html')
        except Exception:
            messages.error(request,"User not found")
            return redirect('/account/login/')
            
def Register(request):
    if request.method == "GET":
        return render(request,'register.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get("email")

        if User.objects.filter(email = email).exists():
            messages.error(request,"Email has been already used!")
            return redirect('/account/register/')
        else:
            
            password = request.POST.get('password')
            password_confirm = request.POST.get('passwordconfirm')
            if password == password_confirm:
                phone = request.POST.get('phone')
                profile = request.FILES.get('profile')
                address = request.POST.get('address')
                user = User.objects.create_user(
                    name = name,
                    email = email,
                    phone = phone,
                    profile = profile,
                    address = address,
                    password = password,
                )

                messages.success(request,"Account was created for "+name)
                return redirect('/account/login/')
            else:
                messages.error(request,"Password does not match! Please check your password again!")
                return redirect('/account/register/')
    else:
        messages.error(request,"Invalid request method!")
        return redirect('/account/register/')

def LogOut(request):
    logout(request)
    return redirect('/account/login/')