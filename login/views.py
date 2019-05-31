from models.models  import *
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import random
import string
import hashlib
import re

# Create your views here.
def login(request):
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        

        
        matchSymbol = re.findall(r'/#@#$%{!{&',password)
        matchDigit = re.findall(r'\d\d\d',password)
        matchLowercase = re.findall(r'[a-z]',password)
        matchUppercase = re.findall(r'[A-Z]',password)


        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        if len(password) < 16 :
            errormsg = "invalid password"
            messages.error(request,errormsg)
            return redirect('login')
        if len(matchSymbol) > 2:
            errormsg = "invalid password no symbol found"
            messages.error(request,errormsg)
            return render(request,'content.html',{}) 
        if len(matchDigit) > 3:
            errormsg = "invalid password no digit found"
            messages.error(request,errormsg)
            return render(request,'content.html',{}) 
        if len(matchLowercase) == 0:
            errormsg = "invalid password no lowercase found"
            messages.error(request,errormsg)
            return render(request,'content.html',{}) 
        if len(matchUppercase) > 2:
            errormsg = "invalid password no uppercase found"
            messages.error(request,errormsg)
            return render(request,'content.html',{}) 
        try:
           user = LoginDetails.objects.get(email=email)
           secret = user.secret
           passwordVerify = EncryptPassword(password+secret)

           if LoginDetail.objects.get(email=email).count()>0:
               errormsg = "Error Multiple Account Found"
               messages.error(request,errormsg)
               return render(request,'content.html',{})
           if passwordVerify == user.password :
                return render(request,'welcome.html',{}) 
           else :
                errormsg = "invalid email or password"
                messages.error(request,errormsg)
                return render(request,'content.html',{})

        except ObjectDoesNotExist:
              errormsg = "User Don't Exist"
              messages.error(request,errormsg)
              return render(request,'content.html',{})
    return render(request,'content.html',{})   

def gen(request):
    LoginDetails.objects.create(
        password= EncrytPassword("AB123456789ab@@$$"),
        secret  = secretGenerator(),
        ip = "",
        email="oyeniyiadedayo@gmail.com")
    return redirect('login')
def secretGenerator():
    letter = string.ascii_lowercase + string.digits + string.punctuation
    return ''.join(random.choice(letter) for i in range(10))

def EncrytPassword(plainpassword):
    password = hashlib.sha256(plainpassword.encode()).hexdigest()
    return password
