from django.urls import path
from . import api

urlpatterns = [
    path('orders/', api.api_order_list, name='api-order-list'),
    path('orders/<int:order_id>/', api.api_order_detail, name='api-order-detail'),
]
