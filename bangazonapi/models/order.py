from django.db import models
from .user import User

class Order(models.Model):

    closed = models.BooleanField(null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
