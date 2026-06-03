from django.db import models
from django.contrib.auth.models import User
from apps.common.models import BaseModel
from apps.products.models import Product


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
