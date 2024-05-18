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


urlpatterns = [
    
   
    path('',views.store,name="store"),
    path('<slug:category_url>',views.store,name='products_by_category'),
    path('<slug:category_url>/<slug:product_url>',views.product_detail,name="product_details"),
    path('search/',views.search,name="search"),
    path('submit_review/<int:product_id>',views.submit_review,name="submit_review"),
   
]
