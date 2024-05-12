from django.urls import path

from . import views

app_name = 'account'


urlpatterns = [
    path('login/',views.LogIn),
    path('register/',views.Register),
    path('logout/',views.LogOut),
    path('confirm-email-to-reset-password/',views.ConfirmEmailToResetPassword),
    path('reset-password/<str:email>/',views.ResetPassword),
    path('reset-password-success/',views.ResetPasswordSuccess),
]