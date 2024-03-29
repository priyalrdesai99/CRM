from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

# Create your models here.
class UserType(models.Model):
    user_type = models.CharField(max_length=100, blank=True)
    user_name =models.CharField(max_length=100,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserType.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.usertype.save()

class Product_details(models.Model):
    name = models.CharField(max_length=100, blank=True)
    cost_price =models.CharField(max_length=100, blank=True)
    sell_price =models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=1000, blank=True)

