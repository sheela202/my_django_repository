"""
URL configuration for my_django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.urls import path,include

urlpatterns = [
    
   
    
    path('',views.carts,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='addcart'),
    path('remove_cart_item/<int:product_id>/',views.remove_cartItem,name='RemoveCartItem'),
    #path('remove_cart_item/<int:product_id>/',views.remove_Item,name='RemoveItem'),
    path('checkout',views.checkout,name="checkout"),
    
] 
