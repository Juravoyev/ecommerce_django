from rest_framework import generics

from apps.orders.api_serializers import OrderSerializer, OrderUpdateSerializer
from apps.orders.models import Order


class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.select_related('user')


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'order_id'

    def get_queryset(self):
        return Order.objects.select_related('user')

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OrderUpdateSerializer
        return OrderSerializer
