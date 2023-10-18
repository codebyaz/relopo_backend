from django.db import models
from django.contrib.auth.models import User
from relopo.products.models import Product

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)