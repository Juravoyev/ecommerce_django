from django.urls import path

from apps.orders.api_endpoints.orders.OrderDetail.views import order_detail_view
from apps.orders.api_endpoints.orders.OrderList.views import order_list_view


urlpatterns = [
    path('', order_list_view, name='api_order_list'),
    path('<int:order_id>/', order_detail_view, name='api_order_detail'),
]
