from django.shortcuts import render

# Create your views here.

def AdminDashboard(request):
    return render(request,"dashboard.html")
