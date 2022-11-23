from queue import Empty
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User ,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import Reader

# Create your views here.

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        userpass = request.POST.get('userpass')
        cpass= request.POST.get('cpass')

        if User.objects.filter(username = username).exists():
            messages.error(request,'This Username already exist, Try with another!!')
            
        elif User.objects.filter(email = email).exists():
            messages.error(request,'This Email already exist, Try with another!!')
        else:
            if userpass != cpass:
                messages.error(request,'Password Miss Match!!')
            elif name =='':
                messages.error(request,'Please Enter your name !!')
            elif username =='':
                messages.error(request,'Please Enter your Username !!')
            elif email =='':
                messages.error(request,'Please Enter your email ')
            elif userpass =='':
                messages.error(request,'Please Enter Password !')
            else:
                user = User.objects.create_user(username = username,email=email, password = userpass,first_name = name) 
                user.save()
                reader = Reader.objects.create(user = user, name = name)
                reader.save()
                
                User.username = username
                User.username = User.username.capitalize()
                messages.success(request,'hello, '+  User.username+' Your Account created Successfully !!')
                return render(request,'signin.html')
    
    
    return render(request,'signup.html')
    


def signin(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request,user)
            User.username = username
            messages.success(request,User.username + '  Login Successfully !!')
            return redirect('/')
        else:
            messages.error(request,'Worng Username or Password')

    return render(request,'signin.html')

def logout(request):
    auth.logout(request)
    messages.success(request,'Logged Out Successfullyy !!')
    return redirect('/')


def changepassword(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            oldpass = request.POST.get('oldpass')
            newpass = request.POST.get('newpass')
            cnewpass = request.POST.get('cnewpass')
            
            user = User.objects.get(id = request.user.id)
            checking = user.check_password(oldpass)
            
            un = user.username
            if checking:
                if newpass != cnewpass:
                    messages.error(request,"Confirm new password didn't match")
                else:
                    user.set_password(newpass)
                    user.save()
                    user = User.objects.get(username = un)
                    auth.login(request,user)
                    messages.success(request,"password changed Successfully !")
            else:
                messages.error(request,"Incorrect old password")


           
                   
                
        return render(request,'changepassword.html' )
    else:
        return redirect('/account/signin/')



# Reset password code
from django.core.mail import send_mail 
import random
from OnBooks.emailauth import emailSubject , emailBody
from django.conf import settings

# HTML email required stuff
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# def resetpassword(request):
#     if request.method =='POST':
#         mail = request.POST['email']

#         try:
#             user = get_object_or_404(User,email = mail)
#             otp = random.randint(2000,9999)
#             try:
#                 email = send_mail(
#                     emailSubject,
#                     emailBody.format(user.username,otp),
#                     settings.EMAIL_HOST_USER,
#                     [mail]
#                 )
#                 messages.success(request,"Reset OTP Sent your email !")
#                 return redirect('/account/resetpassword/?sent=True')
#             except:
#                 messages.error(request,'Somthing went worng ! Please check your connection !')
#         except:
#             messages.error(request,'No user registred with this email')
        
#     return render(request,'resetpassword.html'  )

rotp = 2345
unmail = ""
def resetpassword(request):
    if request.method =='POST':
        global unmail
        mail = request.POST['email']

        try:
            user = get_object_or_404(User,email = mail)
            otp = random.randint(2000,9999)
            global rotp
            rotp = otp
            unmail = user.username
            emailBodyHTML = render_to_string("email_template.html",{'emailSubject':emailSubject,'otpbox':otp,'emailBody':emailBody,'userName':user.username})
            text_content = strip_tags(emailBodyHTML)
            try:
                email = EmailMultiAlternatives(
                    emailSubject,
                    emailBodyHTML,
                    settings.EMAIL_HOST_USER,
                    [mail]
                )
                email.attach_alternative(emailBodyHTML,'text/html')
                email.send()
                messages.success(request,"Reset OTP Sent your email !")
                return redirect('/account/resetpassword/?sent=True')
            except:
                messages.error(request,'Somthing went worng ! Please check your connection !')
        except:
            messages.error(request,'No user registred with this email')
        
    return render(request,'resetpassword.html'  )


def verfiyreset(request):
    if request.method == 'POST':
        votp = int(request.POST['votp'])
        
        if rotp == votp:
            messages.success(request,"correct otp")
            return render(request,"newpassword.html")
        else:
            messages.error(request,"incorrect")
            return redirect('/account/resetpassword/?sent=True')


        
        # chance = 3
        # while rotp != int(votp):
        #     if int(votp) == rotp:
        #         messages.success(request,"verified")
        #         return redirect('/account/signin/')
        #     else:
        #         chance = chance - 1
        #         messages.error(request,"Worng otp you only "+ str(chance) +" try left")
        #         if(chance == 0):
        #             return redirect('/account/resetpassword/?sent=True')
                
    return redirect('/account/resetpassword/')


def setnewpass(request):
    if request.method =='POST':
        newpass = request.POST.get('npass')
        cnewpass = request.POST.get('cnpass')
        
        if newpass != cnewpass:
            messages.error(request,"Confirm Password not match")
            return render(request,"newpassword.html")
        else:
            print(unmail)
            print(newpass)
            user = get_object_or_404(User,username = unmail)
            user.set_password(newpass)
            user.save()
            messages.success(request,"Your Password reset successfully !")
            return redirect('/account/signin/')