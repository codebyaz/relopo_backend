from django.db import models
from django.utils.translation import gettext_lazy as _

from relopo.locations.models import City

# Create your models here.
class Ad(models.Model):
    class PropertyTypes(models.TextChoices):
        FLAT = "F", _("flat")
        PENTHOUSE = "P", _("penthouse")
        DUPLEX = "D", _("duplex")
        STUDIO = "S", _("studio")
        CHALET = "C", _("chalet")
        COUNTRY_HOUSE = "CH", _("country house")

    external_code = models.IntegerField()
    thumbnail = models.CharField(max_length=200)
    floor = models.IntegerField(blank=True, null=True, default=None)
    number_photos = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    property_type = models.CharField(
        max_length=2,
        choices=PropertyTypes.choices,
    )
    size = models.DecimalField(decimal_places=2, max_digits=8)
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    address = models.CharField(max_length=200, blank=True)
    city = models.ForeignKey(City, db_column='slug_name', on_delete=models.PROTECT)
    neighborhood = models.CharField(max_length=200, blank=True)
    district = models.CharField(max_length=200)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    source_url = models.CharField(max_length=200)
    has_lift = models.BooleanField(null=True)