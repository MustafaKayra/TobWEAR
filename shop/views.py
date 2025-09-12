from django.shortcuts import render, redirect
from .models import Product, ProductCategory, OrderItem, ProductColor, ProductSize, ShoppingCard, OrderCard
import json
from django.core.exceptions import ValidationError
import iyzipay


def index(request):
    mostratedproducts1 = Product.objects.filter().order_by("name")[:3]
    mostratedproducts2 = Product.objects.filter().order_by("discounted")[:3]
    mostratedproducts3 = Product.objects.filter().order_by("price")[:3]

    context = {
        "mostratedproducts1": mostratedproducts1,
        "mostratedproducts2": mostratedproducts2,
        "mostratedproducts3": mostratedproducts3
    }

    return render(request,"index.html",context)

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

        if "category" in data or "minimumPriceValue" in data or "maximumPriceValue" in data:
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
        
        elif "productId" in data:
            data = json.loads(request.body)
            productId = data.get("productId")
            colorname = data.get("color")
            sizename = data.get("size")

            color = ProductColor.objects.get(color=colorname)
            size = ProductSize.objects.get(size=sizename)
            product = Product.objects.get(id=productId)
            neworder = OrderItem.objects.create(product=product, color=color, size=size, amount=1)
            print("Yeni Sipariş:", neworder)
            
            if ShoppingCard.objects.get(customer=request.user):
                card = ShoppingCard.objects.get(customer=request.user)
                card.orders.add(neworder)
                print("Ürün Eklendi")
            else:
                newcard = ShoppingCard.objects.create(customer=request.user)
                newcard.orders.add(neworder)
                print("Ürün Yeni Sepete Eklendi")

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

        if OrderItem.objects.filter(product=product):
            raise ValidationError("Bu Üründen Sepette Var!")
        else:
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


def payment(request):
    customer = request.user
    card = ShoppingCard.objects.get(customer=request.user)

    if request.method == "POST":
        options = {
            'api_key': 'sandbox-LC3nNJCVAqA1QZYlFSreYK5VO3nYIDlE',
            'secret_key': 'sandbox-kOflXwc5MbTldBKuogFADjFlrQlKsMfS',
            'base_url': 'sandbox-api.iyzipay.com',
        }

        payment_card = {
            'cardHolderName': customer.first_name +" "+ customer.last_name, #Kart Sahibinin Adı
            'cardNumber': customer.cardnumber, #Kart Numarası
            'expireMonth': customer.cardexpire.split("/")[0].strip(), #Kartın Son Kullanma Ayı
            'expireYear': customer.cardexpire.split("/")[1].strip(), #Kartın Son Kullanma Yılı
            'cvc': customer.cvc, #Kartın Güvenlik Numarası
            'registeredCart': '1' #Kartı Kaydedip Kaydetmeme Durumu '0' Kaydetmez '1' Kaydeder
        }

        buyer = {
            'id': str(customer.id), #Alıcının ID'si
            'name': customer.first_name, #Alıcının Adı
            'surname': customer.last_name, #Alıcının Soyadı
            'gsmNumber': customer.gsmnumber, #Alıcının Telefon Numarası
            'email': customer.email, #Alıcının Emaili
            'identityNumber': '74300864791', #Alıcının Kimlik Numarası
            'lastLoginDate': '2015-10-05 12:43:35', #Alıcının Son Giriş Yaptığı Tarih
            'registrationDate': '2013-04-21 15:12:09', #Alıcının Kayıt Olduğu Tarih
            'registrationAddress': customer.adress, #Alıcının Kayıtlı Olduğu Adresi
            'ip': request.META.get('REMOTE_ADDR'), #Alıcının IP Adresi
            'city': customer.city, #Alıcının Yaşadığı Şehir
            'country': customer.country, #Alıcının Yaşadığı Ülke
            'zipCode': customer.zipcode, #Alıcının Posta Kodu
        }

        address = {
            'contactName': customer.first_name +" "+ customer.last_name, #Adresle İlgili Kişinin Adı
            'city': customer.city, #Şehir
            'country': customer.country, #Ülke
            'address': customer.adress, #Adres Detayları
            'zipCode': customer.zipcode #Posta Kodu
        }

        basket_items = [
            
        ]

        totalprice = 0

        for items in card.orders.all():
            item_total_price = items.totalprice()

            basket_item = {
                "id": str(items.product.id),
                "name": items.product.name,
                "category1": str(items.product.category.name),
                "category2": str(items.product.name),
                "itemType": 'PHYSICAL',
                "price": str(item_total_price),
                "quantity": str(items.amount) 
            }

            totalprice += item_total_price
            basket_items.append(basket_item)


        payment_request = {
            'locale': 'tr', #Dil ve yerel ayar
            'conversationId': '123456789', #İsteğin Konuşma Id'si
            'price': str(totalprice), #Toplam Tutar(Vergiler Hariç)
            'paidPrice': str(totalprice), #Ödenen Toplam Tutar(Vergiler Dahil)
            'currency': 'TRY', #Para Birimi
            'installment': '1', #Taksit Sayısı
            'basketId': str(card.id), #Sepet ID'si
            'paymentChannel': 'WEB', #Ödeme Kanalı
            'paymentGroup': 'PRODUCT', #Ödeme Grubu('PRODUCT' ürün ödemesi için)
            'paymentCard': payment_card, #Ödeme Kartı Bilgileri
            'buyer': buyer, #Alıcı Bilgileri,
            'shippingAddress': address, #Teslimat Adresi
            'billingAddress': address, #Fatura Adresi
            'basketItems': basket_items #Sepet Öğeleri
        }

        payment = iyzipay.Payment().create(payment_request, options)
        payment_result = json.loads(payment.read().decode('utf-8'))
        if payment_result.get("status") == "success":
            print("Ödeme Başarıyla Gerçekleşti, Siparişiniz Hazırlanıyor")
            card.ordered = True
            card.save()
            OrderCard.objects.create(shoppingcard=card)
            return redirect('index')
        elif payment_result.get("status") == "failure":
            print("Ödemeniz Başarısız Oldu, Kart Ve Adres Bilgilerinizi Kontrol Ediniz")
            print(payment_result)
            return redirect('updateuser')