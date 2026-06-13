from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.products.models import Product


class Order(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    address = models.TextField()
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total_price__gte=0),
                name='order_total_price_gte_0',
            ),
        ]

    def calculate_total(self):
        return sum(
            (item.line_total for item in self.items.all()),
            Decimal('0.00'),
        )

    def update_total(self):
        self.total_price = self.calculate_total()
        self.save(update_fields=('total_price', 'updated_at'))

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='order_items',
        null=True,
        blank=True,
    )
    product_name = models.CharField(max_length=255, blank=True)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name='order_item_quantity_gte_1',
            ),
            models.CheckConstraint(
                condition=models.Q(unit_price__gte=0),
                name='order_item_unit_price_gte_0',
            ),
            models.UniqueConstraint(
                fields=('order', 'product'),
                condition=models.Q(product__isnull=False),
                name='unique_product_per_order',
            ),
        ]

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if self.product:
            if not self.product_name:
                self.product_name = self.product.name
            if self._state.adding and self.unit_price == Decimal('0.00'):
                self.unit_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name or self.product} - {self.quantity}"
