from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login,authenticate,logout

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(email=email,password=password)
            if user:
                login(user)
                print("Kullanıcı Başarıyla Giriş Yaptı")
                return redirect('index')
            else:
                print("Böyle Bir Kullanıcı Bulunmuyor")
        else:
            print(form.errors)
    else:
        form = LoginForm()
    return render(request,"login.html",{"form":form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(user)
            print("Kullanıcı Kayıt Oldu")
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request,"register.html",{"form":form})


def updateuser(request):
    return render(request,"updateuser.html")
