from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.orders.api_endpoints.orders.OrderCreate.serializers import OrderCreateSerializer
from apps.orders.api_endpoints.orders.OrderList.serializers import OrderSerializer
from apps.orders.models import Order


@api_view(['GET', 'POST'])
def order_list_view(request):
    if request.method == 'GET':
        orders = Order.objects.select_related('user').all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    serializer = OrderCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
