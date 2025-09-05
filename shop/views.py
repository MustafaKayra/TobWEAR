from django.shortcuts import render
from .models import Product, ProductCategory
import json

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def products(request):
    productobjects = Product.objects.all()
    categories = ProductCategory.objects.filter(product__in=productobjects).distinct()

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {}
        category_name = data.get("category")
        minprice = data.get("minimumPriceValue")
        maxprice = data.get("maximumPriceValue")
        print("Fiyat Filtre Değerleri: ",minprice, maxprice)
        

        if category_name:
            productobjects = productobjects.filter(category__name=category_name)
            print(productobjects)
            print("Kategori Filtresi Çalıştı")

        if minprice:
            print("Minprice kontrolü")
            productobjects = productobjects.filter(price__gte=minprice, category__name=category_name)

        if maxprice:
            print("Maxprice kontrolü")
            productobjects = productobjects.filter(price__lte=maxprice, category__name=category_name)

        return render(request, "partials/product_list.html", {
            "productobjects": productobjects
        })
    
    context = {
        "productobjects": productobjects,
        "categories": categories
    }
    return render(request,"products.html", context)

def shoppingcart(request):
    return render(request,"shoppingcart.html")

def favorites(request):
    return render(request,"favorites.html")

def productdetail(request,slug):
    product = Product.objects.get(slug=slug)
    productfeatures = product.features.all()[:3]
    anotherproducts1 = Product.objects.filter().order_by("discounted")[:4]
    anotherproducts2 = Product.objects.filter(category__name=product.category.name)[:4]
    anotherproducts3 = Product.objects.filter().order_by("price")[:4]
    
    context = {
        "product": product,
        "productfeatures": productfeatures,
        "anotherproducts1": anotherproducts1,
        "anotherproducts2": anotherproducts2,
        "anotherproducts3": anotherproducts3
    }
    return render(request,"productdetail.html",context)
