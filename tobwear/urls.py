from django.contrib import admin
from django.urls import path
from shop import views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('about/',views.about,name="about"),
    path('products/',views.products,name="products"),
    path('shoppingcard/',views.shoppingcart,name="shoppingcard"),
    path('login/',users_views.login,name="login"),
    path('register/',users_views.register,name="register"),
    path('updateuser/',users_views.updateuser,name="updateuser"),
    path('favorites/',views.favorites,name="favorites"),
    path('productdetail/',views.productdetail,name="productdetail")
]
