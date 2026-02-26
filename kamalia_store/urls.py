"""Root URL configuration for kamalia_store project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('users/', include('users.urls')),
    path('api/', include('products.api_urls')),
    path('api/', include('cart.api_urls')),
    path('api/', include('orders.api_urls')),
]

# Serve media files in all environments (static files handled by WhiteNoise)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
