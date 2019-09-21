from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from crmapp.models import Product_details
# Create your models here.


class employee_customer(models.Model):
    customer_name =models.CharField(max_length=100,blank=True)
    customer_id=models.IntegerField()
    employee_id=models.IntegerField()

class transaction(models.Model):
    employee=models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    amount=models.IntegerField(null=False,blank=False)
    date=models.DateField(null=False, blank=False, auto_now=True)
    product=models.ForeignKey(Product_details, on_delete=models.CASCADE,default='-1')

class customer_logins(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    number=models.IntegerField(null=False,blank=False)

class lead_status(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    lead=models.CharField(max_length=100)

