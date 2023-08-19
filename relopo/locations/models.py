from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class City(models.Model):
    class Meta:
        verbose_name_plural = "Cities"
    
    class Countries(models.TextChoices):
        PORTUGAL = "PT", _("Portugal")
        
    name = models.CharField(max_length=100)
    center = models.CharField(max_length=50)
    radius = models.DecimalField(decimal_places=2, max_digits=10)
    is_active = models.BooleanField(default=True)
    country = models.CharField(
        choices=Countries.choices,
        max_length=3,
        default=Countries.PORTUGAL
    )
