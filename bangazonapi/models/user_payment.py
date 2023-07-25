from django.db import models
from .user import User
from .order import Order

class UserPayment(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50)
    user_order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
