from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Product


def home(request):
    """Home page with hero, featured products, and latest products."""
    featured_products = Product.objects.filter(featured=True, in_stock=True)[:8]
    latest_products = Product.objects.filter(in_stock=True)[:8]
    categories = settings.PRODUCT_CATEGORIES
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def product_list(request):
    """Product listing with pagination, category filter, search, and sorting."""
    products = Product.objects.filter(in_stock=True)
    categories = settings.PRODUCT_CATEGORIES
    current_category = request.GET.get('category', '')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')

    if current_category:
        products = products.filter(category=current_category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'products/list.html', context)


def product_detail(request, slug):
    """Single product detail page."""
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    related_products = Product.objects.filter(
        category=product.category, in_stock=True
    ).exclude(pk=product.pk)[:4]
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/detail.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
