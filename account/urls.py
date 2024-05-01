from django.urls import path

from . import views

app_name = 'account'


urlpatterns = [
    path('login/',views.LogIn),
    path('register/',views.Register),
]