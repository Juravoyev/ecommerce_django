from django.urls import path

from apps.products.api_endpoints.products.ProductDetail.views import product_detail_view
from apps.products.api_endpoints.products.ProductList.views import product_list_view


urlpatterns = [
    path('', product_list_view, name='api_product_list'),
    path('<int:product_id>/', product_detail_view, name='api_product_detail'),
]
