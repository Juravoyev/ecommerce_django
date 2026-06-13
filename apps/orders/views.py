from django.shortcuts import render

from .models import Order


def order_list(request):
    orders = (
        Order.objects.select_related('user')
        .prefetch_related('items__product')
        .all()
    )

    if request.user.is_authenticated and not request.user.is_staff:
        orders = orders.filter(user=request.user)

    return render(request, 'orders/order_list.html', {'orders': orders})
