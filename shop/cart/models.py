from django.db import models
from django.urls import reverse

from product.models import Product
from account.models import CustomUser


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=60, default='ACTIVE')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length=3, default='PLN')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def get_delete_url(self):
        return reverse('cart:delete')
