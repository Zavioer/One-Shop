from enum import Enum
from django.db import models
from django.urls import reverse
from account.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_delete_url(self):
        return reverse('product:delete-category', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('product:update-category', kwargs={'pk': self.pk})

class Product(models.Model):
    name = models.CharField(max_length=254)    
    price = models.FloatField(default=0)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:details', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('product:delete', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('product:update', kwargs={'pk': self.pk})
        

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    vote_plus = models.IntegerField(default=0)
    vote_minus = models.IntegerField(default=0)
    bought = models.BooleanField(default=False)


class CommentRate(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vote = models.SmallIntegerField()


class VoteType(Enum):
    minus = 0
    plus = 1
