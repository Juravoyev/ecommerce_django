from rest_framework import serializers

from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'status',
            'full_name',
            'phone',
            'address',
            'total_price',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'total_price',
            'created_at',
            'updated_at',
        )


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status', 'full_name', 'phone', 'address')
