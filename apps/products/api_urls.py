from django.urls import path

from apps.products.api_views import ProductDetailAPIView, ProductListCreateAPIView


urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='api_product_list'),
    path('<int:product_id>/', ProductDetailAPIView.as_view(), name='api_product_detail'),
]
