from rest_framework import generics
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .api_serializers import ProductSerializer
from .pagination import CustomLimitOffsetPagination
from .filters import ProductFilter


class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomLimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category')


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_object(self):
        product = super().get_object()
        if self.request.method == 'GET' and not product.is_active:
            raise NotFound('Product not found.')
        return product