from django.urls import path
from . import api

urlpatterns = [
    path('cart/', api.api_cart_detail, name='api-cart-detail'),
    path('cart/add/<int:product_id>/', api.api_cart_add, name='api-cart-add'),
    path('cart/remove/<int:product_id>/', api.api_cart_remove, name='api-cart-remove'),
]
