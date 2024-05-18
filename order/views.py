import datetime
from django.shortcuts import render
from . forms import OrderForm
from . models import Order
from carts.models import CartItem
import json
from django.template.loader import render_to_string
from django.core.mail import send_mail
from store.models import product
from django.conf import settings
from django.http import JsonResponse
from order.models import Payment,OrderProduct
# Create your views here.
def place_order(request,total=0):
    form=OrderForm
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user,is_active=True)
    for cart_item in cart_items:
        total+=cart_item.product.price*cart_item.quantity
    tax=round(((2/100)*total),2)
    grand_total=round(total+tax,2)
   
    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
                data=Order()
                data.user=current_user
                data.first_name=form.cleaned_data['first_name']
                data.last_name=form.cleaned_data['last_name']
                data.email=form.cleaned_data['email']
                data.phone=form.cleaned_data['phone']
                data.address_line_1=form.cleaned_data['address_line_1']
                data.address_line_2=form.cleaned_data['address_line_2']
                data.city=form.cleaned_data['city']
                data.state=form.cleaned_data['state']
                data.country=form.cleaned_data['country']
                data.order_note=form.cleaned_data['order_note']
                data.order_total=grand_total
                data.tax=tax
                data.ip=request.META.get('REMOTE_ADDR')
                data.save()
                # order_number generation
                yr=int(datetime.date.today().strftime('%Y'))
                dt=int(datetime.date.today().strftime('%d'))
                mt=int(datetime.date.today().strftime('%m'))
                d=datetime.date(yr,mt,dt)
                current_date=d.strftime('%Y%m%d')
                data.order_number=current_date +str(data.id)

                data.save()

                order=Order.objects.filter(user=current_user,is_ordered=False).last
                
                context={
                     'order':order,
                     'cart_items':cart_items,
                     'total':total,
                     'tax':tax,
                     'grand_total':grand_total,
                     
                }
    return render(request,'payments.html',context)

def payments(request):
    body=json.loads(request.body)
      

    order = Order.objects.all().filter(user=request.user,is_ordered=False).last()
    
    paymentobject = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']
    )

    paymentobject.save()

    order.payment = paymentobject
    order.is_ordered = True
    order.save()

    #Move the cart items to Order product table

    cart_items = CartItem.objects.filter(user=request.user,is_active=True)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id 
        orderproduct.payment = paymentobject 
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity   
        orderproduct.product_price = item.product.price 
        orderproduct.ordered = True
        orderproduct.save()


         #reduce the quantity of cart item.
        productObj = product.objects.get(id = item.product_id)
        productObj.stock = item.quantity
        productObj.save()

        #clear cart
    CartItem.objects.filter(user=request.user).delete()

       

       #send order completion mail to user
    mail_subject = "DAKart - Your Order is Placed"
    email_from = settings.EMAIL_HOST_USER
    message = render_to_string('order_received.html',{
                 'user':request.user,
                 'order':order                         
                 
    })
    to_email = [request.user.email,]
    send_mail(mail_subject,message,email_from,to_email)
    
    print(order.order_number)
    print(paymentobject.payment_id)
        #redirect to order complete page
    data = {
            'order_number':order.order_number,
            'transID':paymentobject.payment_id
    }

    return JsonResponse(data)


def order_complete(request,order_products=None,sub_total=0):
     order_number=request.GET.get('order_number')
     transID=request.GET.get('payment_id')
     order=Order.objects.get(order_number=order_number,is_ordered=True)
     try:
          order_products=OrderProduct.objects.filter(order_id=order.id)
     except:
          pass
     paymentObj=Payment.objects.get(payment_id=transID)
     if order_products.count()>1:
        for i in order_products:
             sub_total+=i.product_price*i.quantity
     else:
          sub_total = order_products.product_price

     context={'order':order,
              'order_products':order_products,
              'transID':transID,
              'payment':paymentObj,
              'order_number':order_number,
              'sub_total':sub_total
              }
     
     return render(request,'order_complete.html',context)

     