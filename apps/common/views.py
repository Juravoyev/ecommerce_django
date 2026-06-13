from django.shortcuts import render

from apps.products.models import Category, Product


def home(request):
    products = (
        Product.objects.filter(is_active=True)
        .select_related('category')
        .order_by('-created_at')[:8]
    )
    categories = (
        Category.objects.filter(is_active=True)
        .prefetch_related('products')
        .order_by('name')[:6]
    )
    return render(
        request,
        'common/home.html',
        {
            'products': products,
            'categories': categories,
        },
    )
