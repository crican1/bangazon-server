from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import UserPayment, User, Order

class UserPaymentView(ViewSet):
    """Bangazon user_payment view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user_payment
        Returns:
            Response -- JSON serialized user_payment
        """
        try:
            user_payment = UserPayment.objects.get(pk=pk)
            serializer = UserPaymentSerializer(user_payment)
            return Response(serializer.data)
        except UserPayment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all user_payments

        Returns:
            Response -- JSON serialized list of user_payments
        """
        user_payment = UserPayment.objects.all()
        serializer = UserPaymentSerializer(user_payment, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized UserPayment instance
        """

        user_id = User.objects.get(pk=request.data["user_id"])
        user_order_id = Order.objects.get(pk=request.data["order_id"])

        user_payment = UserPayment.objects.create(
            user_id=user_id,
            payment_type=request.data["payment_type"],
            user_order_id=user_order_id
        )
        serializer = UserPaymentSerializer(user_payment)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a user_payment

        Returns:
        Response -- Empty body with 204 status code
        """

        user_payment = UserPayment.objects.get(pk=pk)
        user_payment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete UserPayment
        """
        user_payment = UserPayment.objects.get(pk=pk)
        user_payment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class  UserPaymentSerializer(serializers.ModelSerializer):
    """JSON serializer for orders
    """

    class Meta:
        model = UserPayment
        fields = ('id', 'user_id', 'payment_type', 'user_order_id')
        depth = 1
