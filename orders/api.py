from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'name', 'phone', 'email', 'address', 'city', 'state',
             'payment_method', 'total_price', 'status',
            'ordered_at', 'items',
        ]


@api_view(['GET'])
@permission_classes([AllowAny])
def api_order_list(request):
    """List orders for the authenticated user."""
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        return Response({'detail': 'Authentication required'}, status=401)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_order_detail(request, order_id):
    """Retrieve a single order."""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'detail': 'Not found'}, status=404)
    serializer = OrderSerializer(order)
    return Response(serializer.data)
