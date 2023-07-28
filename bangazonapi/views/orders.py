from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Order, User

class OrderView(ViewSet):
    """Bangazon orders view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single order
        Returns:
            Response -- JSON serialized order
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all orders

        Returns:
            Response -- JSON serialized list of orders
        """
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized Order instance
        """
        user_id = User.objects.get(pk=request.data["user_id"])

        order = Order.objects.create(
            closed=request.data["closed"],
            created_on=datetime.now(),
            user_id=user_id
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a order

        Returns:
        Response -- Empty body with 204 status code
        """

        order = Order.objects.get(pk=pk)
        order.closed = request.data["closed"]
        order.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete Order
        """
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class  OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for orders
    """

    created_on = serializers.DateTimeField(format="%B %d, %Y, %I:%M%p")

    class Meta:
        model = Order
        fields = ('id', 'closed', 'created_on', 'user_id')
        depth = 1
