from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Order, Product, OrderProduct

class OrderProductView(ViewSet):
    """Bangazon order products view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single order
        Returns:
            Response -- JSON serialized order
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(order_product)
            return Response(serializer.data)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all order products

        Returns:
            Response -- JSON serialized list of order products
        """

        order_id = request.query_params.get('orderId', None)
        order_product = OrderProduct.objects.all().filter(order_id=order_id)

        order_product = OrderProduct.objects.all()
        serializer = OrderProductSerializer(order_product, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized Order Product instance
        """
        order_id = Order.objects.get(pk=request.data["orderId"])
        order_item_id = Product.objects.get(pk=request.data["productId"])

        order_product = OrderProduct.objects.create(
            order_id=order_id,
            order_item_id=order_item_id
        )

        serializer = OrderProductSerializer(order_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a order product
        
        Returns -- Empty body with 204 status code
        """

        comment = Comment.objects.get(pk=pk)
        comment.content = request.data["content"]
        # comment.created_on = request.data["created_on"]

        # author_id = User.objects.get(pk=request.data["authorId"])
        # comment.author_id = author_id

        # post_id = Post.objects.get(pk=request.data["postId"])
        # comment.post_id = post_id

        comment.save()

        return Response(None, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """Delete order products
        """
        order_product = OrderProduct.objects.get(pk=pk)
        order_product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class  OrderProductSerializer(serializers.ModelSerializer):
    """JSON serializer for order products
    """

    class Meta:
        model = OrderProduct
        fields = ('id', 'order_id', 'order_item_id')
        depth = 1
