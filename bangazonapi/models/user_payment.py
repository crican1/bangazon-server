from django.db import models
from .user import User
from .order import Order
from .payment import Payment

class UserPayment(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(Payment, on_delete=models.CASCADE)
    user_order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
