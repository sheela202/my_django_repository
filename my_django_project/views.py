from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

from store.models import product

def indexpage(request):
    products=product.objects.all().filter(is_available=True)
    context={'products':products}
    return render(request,'index.html',context)
