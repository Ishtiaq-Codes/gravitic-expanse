from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'description', 'price',
            'discount_price', 'image', 'in_stock', 'effective_price',
            'discount_percentage', 'created_at',
        ]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(in_stock=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
