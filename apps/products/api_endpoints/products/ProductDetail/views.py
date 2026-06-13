from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.products.api_endpoints.products.ProductDetail.serializers import ProductDetailSerializer
from apps.products.api_endpoints.products.ProductUpdateDestroy.serializers import ProductUpdateSerializer
from apps.products.models import Product


@api_view(['GET', 'PATCH', 'DELETE'])
def product_detail_view(request, product_id):
    try:
        product = Product.objects.select_related('category').get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    if request.method == 'GET':
        if not product.is_active:
            return Response({'error': 'Product not found'}, status=404)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = ProductUpdateSerializer(
            product,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    product.delete()
    return Response(status=204)
