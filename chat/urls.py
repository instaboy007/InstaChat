from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.LoginPage, name='Login'),
    path('SignUp/', views.SignUpPage, name='SignUp'),
    path('ForgotPassword/', views.ForgotPasswordPage, name='ForgotPassword'),
    path('OTP/', views.OTPPage, name='Otp'),
    path('ResetPassword/', views.ResetPasswordPage, name='ResetPassword'),
    path('ProfilePicture/', views.ProfilePicturePage, name='ProfilePicture'),
    path('chat/<str:room_name>/', views.room, name='room'),
]