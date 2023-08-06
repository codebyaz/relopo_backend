from django.db import models
from typing import List, Text 

from .enums import ProductTypeEnum

# Create your models here.
class Product(models.Model):
    name: Text = models.CharField(max_length=30)
    description: Text = models.CharField(max_length=200, default=None, blank=True)
    price: float = models.DecimalField(max_digits=5, decimal_places=2)
    type: List[ProductTypeEnum] = models.CharField(max_length=10, choices=ProductTypeEnum.choices)