from django.shortcuts import render, redirect
from .models import Product, ProductCategory, OrderItem, ProductColor, ProductSize, ShoppingCard, OrderCard
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
    if ShoppingCard.objects.filter(customer=request.user):
        shoppingcard = ShoppingCard.objects.get(customer=request.user)
        context = {
            "shoppingcard": shoppingcard
        }

    if request.method == "POST":
        data = json.loads(request.body)

        if "orderQuantity" in data:
            orderquantity = data.get("orderQuantity")
            orderid = data.get("orderId")
            order = OrderItem.objects.get(id=orderid)
            order.amount = orderquantity
            order.save()
            print("Order: ", order)
            print("Order Amount: ", order.amount)      

        if "orderDelete" in data:
            orderid = data.get("orderId")
            order = OrderItem.objects.get(id=orderid)
            order.delete()

    return render(request,"shoppingcart.html",context)

def favorites(request):
    return render(request,"favorites.html")

def productdetail(request,slug):
    product = Product.objects.get(slug=slug)
    productfeatures = product.features.all()[:3]
    anotherproducts1 = Product.objects.filter().order_by("discounted")[:4]
    anotherproducts2 = Product.objects.filter(category__name=product.category.name)[:4]
    anotherproducts3 = Product.objects.filter().order_by("price")[:4]

    if request.method == "POST":
        data = json.loads(request.body)
        amount = data.get("number")
        colorname = data.get("color")
        sizename = data.get("size")

        color = ProductColor.objects.get(color=colorname)
        size = ProductSize.objects.get(size=sizename)
        neworder = OrderItem.objects.create(product=product,amount=amount,color=color,size=size)

        if ShoppingCard.objects.filter(customer=request.user).exists():
            card = ShoppingCard.objects.get(customer=request.user)
            card.orders.add(neworder)
            print("Alışveriş Sepetine Ürün Eklendi")
        else:
            newcard = ShoppingCard.objects.create(customer=request.user)
            newcard.orders.add(neworder)
            print("Alışveriş Sepeti Oluşturuldu")
            

    
    context = {
        "product": product,
        "productfeatures": productfeatures,
        "anotherproducts1": anotherproducts1,
        "anotherproducts2": anotherproducts2,
        "anotherproducts3": anotherproducts3
    }
    return render(request,"productdetail.html",context)
