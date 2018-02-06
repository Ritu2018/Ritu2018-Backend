from django.db import models


# Create your models here.

class TransactionModel(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    email = models.EmailField()
    product_info = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
