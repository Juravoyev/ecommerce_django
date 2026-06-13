from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.orders.api_endpoints.orders.OrderUpdateDestroy.serializers import OrderUpdateSerializer
from apps.orders.models import Order

@api_view(['PATCH', 'DELETE'])
def order_update_destroy_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)

    if request.method == 'PATCH':
        serializer = OrderUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=204)
