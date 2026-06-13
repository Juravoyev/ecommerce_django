from rest_framework import serializers

from apps.orders.models import Order

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
