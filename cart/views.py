from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart


def cart_detail(request):
    """Display cart contents."""
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    """Add product to cart (supports AJAX)."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, in_stock=True)
    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override') == 'true'
    cart.add(product, quantity=quantity, override_qty=override)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'message': f'{product.name} added to cart',
        })
    return redirect('cart_detail')


@require_POST
def cart_update(request, product_id):
    """Update product quantity in cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(product, quantity)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'total': str(cart.get_total_price()),
        })
    return redirect('cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Remove product from cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'total': str(cart.get_total_price()),
        })
    return redirect('cart_detail')
