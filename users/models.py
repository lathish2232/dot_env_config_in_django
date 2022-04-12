from lib2to3.pgen2 import token
from django.db import models

# Create your models here.

class Users(models.Model):
    
    #REQUIRED_FIELDS = []
    class Meta:
        db_table = 'users'

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255 ,verbose_name='email address', unique=True)
    phone_number = models.CharField(max_length=22,unique=True)
    Subject=models.CharField(max_length=100)
    Message= models.CharField(max_length=100)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    last_login = models.DateTimeField(auto_now_add=True)
    address_id = models.IntegerField()
    token =models.PositiveIntegerField(null=True, blank=True)
    


    


