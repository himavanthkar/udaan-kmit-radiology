from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib.auth.models import User,auth

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        check = request.POST['userLogin']

        #print(check)

        user = auth.authenticate(username = username, password = password)
        # print(user.is_superuser)
        if user is not None:
            if (user.is_superuser and check == 'true'):
                messages.info(request, "Doctors/Pathalogists please sign in using other form")
                return redirect("auths:login")
            elif (user.is_superuser == False and check == 'isAdmin'):
                messages.info(request, "Users please sign in using other form")
                return redirect("auths:login")
            else:
                auth.login(request, user)
                return redirect("/")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("auths:login")
    else:
        return render(request,"auths/login.html")

def Logout(request):
    auth.logout(request)
    return redirect("/")