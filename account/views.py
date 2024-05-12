from django.shortcuts import render,redirect
from account.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import check_password
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def generate_random_code():
    from random import randrange 
    random_code = randrange(1000000000, 9999999999) 
    return random_code

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
                if user.role == "admin":
                    messages.success(request, "You are now logged in as "+ username)
                    return redirect('/myadmin/dashboard/')
                else:
                    messages.success(request, "You are now logged in as "+ username)
                    return redirect('/')
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
                    account_number = generate_random_code(),
                    name = name,
                    email = email,
                    phone = phone,
                    profile = profile,
                    address = address,
                    password = password,
                )

                subject = 'welcome to GFG world'
                message = f'{user.name}, thank you'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                send_mail( subject,message,email_from,recipient_list)

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

def ConfirmEmailToResetPassword(request):
    if request.method == "GET":
        return render(request,"confirm-email-to-reset-password.html")
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email = email).exists():
            return redirect('/account/reset-password/' + email + '/')
        else:
            messages.error(request,"Email does not found!")
            return redirect('/account/confirm-email-to-reset-password/')
        
def ResetPassword(request,email):
    if request.method == "GET":
        return render(request,"reset-password.html",{"email":email})
    if request.method == "POST":
        password = request.POST.get('password')
        passwordconfirm = request.POST.get('passwordconfirm')
        if password == passwordconfirm:
            user = User.objects.filter(email = email).first()
            user.set_password(passwordconfirm)
            user.save()

            return redirect('/account/reset-password-success/')
        else:
            messages.error(request,"Password does not match! Please check your password again!")
            return redirect('/account/reset-password/' + email + '/')

def ResetPasswordSuccess(request):
    return render(request,"reset-password-success.html")