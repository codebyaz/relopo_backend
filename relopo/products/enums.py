from django.db.models import TextChoices

class ProductTypeEnum(TextChoices):
    service = "service"