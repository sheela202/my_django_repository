
from . views import *
from . models import Cart,CartItem
def cartCounter(request):
    cart_count=0
    try:
        if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user,is_active=True)
        else:
           cart=Cart.objects.get(cart_id=cart_id(request))
           cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
                cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count=0
    return dict(count=cart_count)


 