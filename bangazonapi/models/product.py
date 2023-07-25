from django.db import models

class Product(models.Model):

    product_image = models.URLField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    price = models.IntegerField()
    units_available = models.IntegerField()
  