from django import forms
from django.forms import fields
from .models import UserAccount

class UserRegistrationForm(forms.ModelForm):
    Email=forms.EmailField()
    UserID=forms.CharField(max_length=30)
    Password=forms.CharField(widget = forms.PasswordInput())
    RetypePassword=forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model=UserAccount
        fields=['UserID','Email','Password']

class UserLoginForm(forms.Form):
    UserID=forms.CharField(max_length=30)
    Password=forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model=UserAccount
        fields=['UserID','Password']

class ForgotPasswordForm(forms.Form):
    Email = forms.EmailField()
    class Meta:
        model=UserAccount
        fields=['Email']

class OTPForm(forms.Form):
    Otp=forms.CharField(max_length=4)

class ResetPasswordForm(forms.Form):
    newPassword=forms.CharField(widget = forms.PasswordInput())
    reTypeNewPassword=forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model=UserAccount
        fields=['Email','Password']

