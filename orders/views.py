from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


def checkout(request):
    """Checkout page: display form and process order."""
    cart = Cart(request)

    if cart.is_empty:
        messages.warning(request, 'Your cart is empty. Add some products first!')
        return redirect('product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data.get('email', ''),
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                # postal_code=form.cleaned_data['postal_code'],
                payment_method=form.cleaned_data['payment_method'],
                total_price=cart.get_total_price(),
            )
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Create order items from cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                    suite_code=item['product'].suite_code,
                )

            # Clear the cart
            cart.clear()

            return redirect('order_confirmation', order_id=order.id)
    else:
        # Pre-fill form for logged-in users
        initial = {}
        if request.user.is_authenticated:
            initial['name'] = request.user.get_full_name() or request.user.username
            initial['email'] = request.user.email
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'orders/checkout.html', context)


def order_confirmation(request, order_id):
    """Thank you page with order summary."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/confirmation.html', {'order': order})


def my_orders(request):
    """Show orders by IDs stored in the browser localStorage (passed as ?ids=1,2,3)."""
    ids_param = request.GET.get('ids', '')
    order_ids = []
    for part in ids_param.split(','):
        part = part.strip()
        if part.isdigit():
            order_ids.append(int(part))

    orders = []
    if order_ids:
        orders = list(Order.objects.filter(id__in=order_ids).prefetch_related('items__product'))

    return render(request, 'orders/my_orders.html', {'orders': orders})
