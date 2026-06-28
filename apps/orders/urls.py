from django.urls import path

from .views import order_list, checkout_view

urlpatterns = [
    path('', order_list, name='order_list'),
    path('checkout/', checkout_view, name='checkout'),
]
