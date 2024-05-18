from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address_line_1=models.CharField(max_length=100,blank=True)
    address_line_2=models.CharField(max_length=100,blank=True)
    profile_picture=models.ImageField(upload_to='userprofie',blank=True)
    city=models.CharField(max_length=20,blank=True)
    state=models.CharField(max_length=20,blank=True)
    country=models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.user.first_name