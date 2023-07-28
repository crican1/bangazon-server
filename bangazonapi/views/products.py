from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Product

class ProductView(ViewSet):
    """Bangazon products view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single product
        Returns:
            Response -- JSON serialized product
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all products

        Returns:
            Response -- JSON serialized list of products
        """
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized Product instance
        """

        product = Product.objects.create(
            product_image=request.data["productImage"],
            title=request.data["title"],
            description=request.data["description"],
            price=request.data["price"],
            units_available=request.data["unitsAvailable"],
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a product

        Returns:
        Response -- Empty body with 204 status code
        """

        product = Product.objects.get(pk=pk)
        product.product_image = request.data["productImage"]
        product.title = request.data["title"]
        product.description = request.data["description"]
        product.price = request.data["price"]
        product.units_available = request.data["unitsAvailable"]
        product.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete Product
        """
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class  ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for productss
    """
    class Meta:
        model = Product
        fields = ('id', 'product_image', 'title', 'description', 'price', 'units_available')
        depth = 1
