from django.urls import path

from apps.orders.api_views import OrderDetailAPIView, OrderListCreateAPIView


urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='api_order_list'),
    path('<int:order_id>/', OrderDetailAPIView.as_view(), name='api_order_detail'),
]
