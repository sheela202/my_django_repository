from django.shortcuts import get_object_or_404, redirect, render
from store.models import product

from django.http import HttpResponse
from category.models import category
from store.models import product
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from .forms import ReviewForm
from store.models import ReviewRating
from django.contrib import messages
from order.models import OrderProduct
# Create your views here.


def store(request,category_url=None):
       if(category_url!=None):
              categories=get_object_or_404(category,slug=category_url)
              products=product.objects.filter(category=categories,is_available=True)
              product_count=products.count()
       else:
              products=product.objects.all().filter(is_available=True)
              product_count=products.count()

       paginator=Paginator(products,3)
       page=request.GET.get('page')
       product_paged=paginator.get_page(page)

       context={
                'products':product_paged,
                'product_count':product_count
                }
       return render(request,'store.html',context)   



def product_detail(request,category_url,product_url,single_product=None):
    
    try:
        single_product = product.objects.get(category__slug=category_url,slug=product_url)
        #print(Product.objects.get(category__slug=category_url,slug=product_url).query)
    except:
        pass
        
    reviews = ReviewRating.objects.filter(product_id = single_product.id, status=True)
    
    Order_product = OrderProduct.objects.filter(user__id = request.user.id,product_id=single_product.id).last()
    context = {
        'single_product':single_product,
        'reviews':reviews,
        'Order_product':Order_product
    }
    
    return render(request,'product_detail.html', context)

def search(request):
       if 'keyword' in request.GET:
              keyword=request.GET['keyword']
              products=product.objects.filter(Q(slug__icontains=keyword) | Q(product_name__icontains=keyword))
              product_count=products.count

              context={
                     'products':products,
                     'product_count':product_count
              }
       return render(request,'store.html',context)



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.POST['rating'] == "":
        messages.error(request,"Rating is required")
    else:
        if request.method == 'POST':
            try:
                reviews = ReviewRating.objects.get(user__id = request.user.id,product__id = product_id)
                form = ReviewForm(request.POST,instance=reviews)
                form.save()
                messages.success(request,"Thank you! your review has been submitted")
                return redirect(url)
            except ReviewRating.DoesNotExist:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    data = ReviewRating()
                    data.subject = form.cleaned_data['subject']
                    data.rating = form.cleaned_data['rating']
                    data.review = form.cleaned_data['review']
                    data.ip = request.META.get('REMOTE_ADDR')
                    data.product_id = product_id
                    data.user_id = request.user.id
                    data.save()
                    messages.success(request,"Thank you! your review has been Created")
    return redirect(url)


