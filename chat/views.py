from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserLoginForm,ForgotPasswordForm,OTPForm,ResetPasswordForm
from django.contrib import messages
from .models import UserAccount
from django.core.mail import EmailMessage
from django.conf import settings
import random

ResetPassword={}

def index(request):
    return render(request, 'chat/index.html')

def LoginPage(Request):
    if Request.method=='GET':
        Login=UserLoginForm(Request.GET)
        UserData=UserAccount.objects.all()
        global UserID
        if Login.is_valid():
            UserID = Login.cleaned_data['UserID']
            Password=Login.cleaned_data['Password']
            userFlag=0
            for user in UserData:
                if UserID==user.UserID and Password==user.Password:
                    userFlag==1
                    return redirect('/chat/lobby/?name=lobby&user='+UserID)
            if userFlag==0:
                messages.error(Request,'Account Doesnt Exist! Try Creating One.')
        else:
            Login=UserLoginForm()
    return render(Request,'Login/Login.html',{'title':'Login'})

def SignUpPage(Request):
    if Request.method == "POST":
        SignUp = UserRegistrationForm(Request.POST)
        UserData=UserAccount.objects.all()
        if SignUp.is_valid():
            UserID = SignUp.cleaned_data['UserID']
            Email=SignUp.cleaned_data['Email']
            Password=SignUp.cleaned_data['Password']
            RetypePassword=SignUp.cleaned_data['RetypePassword']
            userFlag=0
            for user in UserData:
                if UserID == user.UserID:
                    userFlag=1
                    break
            if userFlag==0 and Password==RetypePassword:
                SignUp.save()
                messages.success(Request, f"Hey, {UserID}!")
                return redirect('ProfilePicture')
            elif userFlag==1:
                messages.error(Request,"User Name or Email Already Exists!")
            elif Password!=RetypePassword:
                messages.error(Request, "Passwords Do Not Match!.")
        else:
            SignUp = UserRegistrationForm()
    return render(Request,'Login/SignUp.html',{'title':'SignUp'})


def ForgotPasswordPage(Request):
    if Request.method=='GET':
        ForgotPassword=ForgotPasswordForm(Request.GET)
        UserData=UserAccount.objects.all()
        if ForgotPassword.is_valid():
            Email=ForgotPassword.cleaned_data['Email']
            userFlag=0
            for user in UserData:
                if Email==user.Email:
                    userFlag==1
                    messages.success(Request, f"OTP Sent to Your Mail ID !")
                    O_T_P = str(random.randint(1000,9999))
                    ResetPassword[Email]=O_T_P
                    messageContent=f'Hi,\n      We got a Request to Reset your InstaChat Password.\n    Your OTP is {O_T_P}. If you Ignore this message your Password will not be Changed. '
                    msg = EmailMessage('InstaChat - Password Reset', messageContent,settings.EMAIL_HOST_USER,[Email])
                    msg.send()
                    return redirect('Otp')  
            print(userFlag)
            if userFlag==0:
                messages.error(Request,"Un-Registered Email ID !")  
        else:
            ForgotPassword = ForgotPasswordForm()
    return render(Request,'Login/ForgotPassword.html',{'title':'ForgotPassword'})

def OTPPage(Request):
    if Request.method=='GET':
        FormOTP=OTPForm(Request.GET)
        if FormOTP.is_valid():
            Otp=FormOTP.cleaned_data['Otp']
            if Otp in ResetPassword.values():
                return redirect('ResetPassword')
            else:
                messages.error(Request,"Invalid OTP!")
        else:
            FormOTP=OTPForm()
    return render(Request,'Login/Otp.html',{'title':'Otp'})

def ResetPasswordPage(Request):
    if Request.method=='POST':
        FormResetPassword=ResetPasswordForm(Request.POST)
        UserData=UserAccount.objects.all()
        if FormResetPassword.is_valid():
            newPassword=FormResetPassword.cleaned_data['newPassword']
            reTypeNewPassword=FormResetPassword.cleaned_data['reTypeNewPassword']
            print(newPassword,reTypeNewPassword)
            print(ResetPassword)
            for key,values in ResetPassword.items():
                EmailKey=key
                break
            if newPassword==reTypeNewPassword:
                i=0
                for user in UserData:
                    if EmailKey==user.Email:
                        user.Password=newPassword
                        UserData[i].save()
                        messages.success(Request,'Reset Password Succesful !')
                        return redirect('Login')
                    i+=1
            elif newPassword!=reTypeNewPassword:
                messages.error(Request,'Passwords do not Match !')
        else:
            FormResetPassword=ResetPasswordForm()
    return render(Request,'Login/ResetPassword.html',{'title':'Reset Password'})

def ProfilePicturePage(Request):
    return render(Request,'Login/ProfilePicture.html',{'title':'ProfilePicture'})

def room(request, room_name):
    name=request.GET["name"]
    user=request.GET["user"]
    return render(request, 'chat/room.html', {'room_name': room_name,'name' : name,'user': user})
