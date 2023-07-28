from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Payment

class PaymentView(ViewSet):
    """Bangazon payments view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single payment
        Returns:
            Response -- JSON serialized payment
        """
        try:
            payment = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        except Payement.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all payments

        Returns:
            Response -- JSON serialized list of payments
        """
        payment = Payment.objects.all()
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized Payment instance
        """

        payment = Payment.objects.create(
            payment_type=request.data["Payment_type"],
        )
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a payment

        Returns:
        Response -- Empty body with 204 status code
        """

        payment = Payment.objects.get(pk=pk)
        payment.payment_type = request.data["payment_type"]
        payment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete Payment
        """
        payment = Payment.objects.get(pk=pk)
        payment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class  PaymentSerializer(serializers.ModelSerializer):
    """JSON serializer for payments
    """
    class Meta:
        model = Payment
        fields = ('id', 'payment_type')
        depth = 1
