from django.db import models

# Create your models here.
from store.models import product
from django.contrib.auth.models import User


class Cart(models.Model):
    cart_id=models.CharField(max_length=200,blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.product_name
    
    def get_subtotal(self):
        return self.product.price * self.quantity