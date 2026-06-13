from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True)
    query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(sku__icontains=query)
        )

    if selected_category:
        products = products.filter(category_id=selected_category)

    return render(
        request,
        'products/product_list.html',
        {
            'products': products,
            'categories': categories,
            'query': query,
            'selected_category': selected_category,
        },
    )


def category_list(request):
    categories = (
        Category.objects.filter(is_active=True)
        .prefetch_related('products')
        .order_by('name')
    )
    return render(
        request,
        'products/category_list.html',
        {'categories': categories},
    )


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk, is_active=True)
    products = category.products.filter(is_active=True).select_related('category')
    return render(
        request,
        'products/category_detail.html',
        {'category': category, 'products': products},
    )
