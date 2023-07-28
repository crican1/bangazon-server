from django.db import models

class Payment(models.Model):

    payment_type = models.CharField(max_length=50)
