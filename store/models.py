from django.db import models
from category.models import category
from django.contrib.auth.models import User
# Create your models here.

class product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug= models.TextField(max_length=500,unique=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to="photos/products")
    stock=models.IntegerField()
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    modified_date=models.DateField(auto_now_add=True)
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return self.product_name
    
class ReviewRating(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=500,blank=True)
    rating=models.FloatField()
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject