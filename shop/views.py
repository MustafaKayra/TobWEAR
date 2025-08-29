from django.shortcuts import render

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def products(request):
    return render(request,"products.html")

def shoppingcart(request):
    return render(request,"shoppingcart.html")

def favorites(request):
    return render(request,"favorites.html")

def productdetail(request):
    return render(request,"productdetail.html")
