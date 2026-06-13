from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.products.api_endpoints.products.ProductCreate.serializers import ProductCreateSerializer
from apps.products.models import Product
from apps.products.api_endpoints.products.ProductList.serializers import ProductSerializer


@api_view(['GET', 'POST'])
def product_list_view(request):
    if request.method == 'GET':
        products = Product.objects.filter(is_active=True).select_related('category')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    serializer = ProductCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
