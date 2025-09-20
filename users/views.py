from django.shortcuts import render, redirect
from .models import CustomUser
from shop.models import Product, ProductCategory
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login,authenticate,logout

def loginuser(request):
    footerproducts = Product.objects.filter()[:5]
    footercategorys = ProductCategory.objects.filter()[:5]

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email,password=password)
            if user:
                login(request, user)
                print("Kullanıcı Başarıyla Giriş Yaptı")
                return redirect('index')
            else:
                print("Böyle Bir Kullanıcı Bulunmuyor")
        else:
            print(form.errors)
    else:
        form = LoginForm()
    return render(request,"login.html",{"form":form, "footerproducts":footerproducts, "footercategorys":footercategorys})


def register(request):
    footerproducts = Product.objects.filter()[:5]
    footercategorys = ProductCategory.objects.filter()[:5]

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("Kullanıcı Kayıt Oldu")
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request,"register.html",{"form":form, "footerproducts":footerproducts, "footercategorys":footercategorys})


def updateuser(request):
    footerproducts = Product.objects.filter()[:5]
    footercategorys = ProductCategory.objects.filter()[:5]

    if request.method == "POST":
        form = RegisterForm(request.POST, instance=request.user)
        if form.is_valid():
            newuser = form.save()
            login(request, newuser)
            print("Kullanıcı Bilgileri Düzenlendi")
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request,"updateuser.html",{"form":form, "footerproducts":footerproducts, "footercategorys":footercategorys})
