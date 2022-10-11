from django.db import models

# Create your models here.

class VwMostSoldProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField() 
    amount = models.IntegerField()
    total = models.FloatField()

    class Meta:
        managed = False
        db_table = 'vw_most_sold_product'
