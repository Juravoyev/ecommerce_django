from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.orders.api_endpoints.orders.OrderCreate.serializers import OrderCreateSerializer



@api_view(['POST'])
def order_create_view(request):
    serializer = OrderCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
