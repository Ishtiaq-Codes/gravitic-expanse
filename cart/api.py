from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from products.models import Product
from .cart import Cart


@api_view(['GET'])
@permission_classes([AllowAny])
def api_cart_detail(request):
    cart = Cart(request)
    items = []
    for item in cart:
        items.append({
            'product_id': item['product'].id,
            'name': item['product'].name,
            'price': str(item['price']),
            'quantity': item['quantity'],
            'total_price': str(item['total_price']),
            'image': item['product'].image.url if item['product'].image else None,
        })
    return Response({
        'items': items,
        'total': str(cart.get_total_price()),
        'count': len(cart),
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def api_cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, in_stock=True)
    quantity = int(request.data.get('quantity', 1))
    cart.add(product, quantity=quantity)
    return Response({'success': True, 'cart_count': len(cart)})


@api_view(['POST'])
@permission_classes([AllowAny])
def api_cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return Response({'success': True, 'cart_count': len(cart)})
