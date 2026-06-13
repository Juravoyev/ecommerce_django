from decimal import Decimal

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def copy_product_snapshot(apps, schema_editor):
    OrderItem = apps.get_model('orders', 'OrderItem')

    for item in OrderItem.objects.select_related('product').iterator():
        item.product_name = item.product.name
        item.unit_price = item.product.price
        item.save(update_fields=('product_name', 'unit_price'))


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('products', '0002_expand_catalog_models'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'),
                    ('processing', 'Processing'),
                    ('shipped', 'Shipped'),
                    ('delivered', 'Delivered'),
                    ('cancelled', 'Cancelled'),
                ],
                default='pending',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('0.00'),
                max_digits=12,
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='unit_price',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('0.00'),
                max_digits=10,
            ),
        ),
        migrations.RunPython(
            copy_product_snapshot,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='order_items',
                to='products.product',
            ),
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.CheckConstraint(
                condition=models.Q(('total_price__gte', 0)),
                name='order_total_price_gte_0',
            ),
        ),
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.CheckConstraint(
                condition=models.Q(('quantity__gte', 1)),
                name='order_item_quantity_gte_1',
            ),
        ),
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.CheckConstraint(
                condition=models.Q(('unit_price__gte', 0)),
                name='order_item_unit_price_gte_0',
            ),
        ),
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.UniqueConstraint(
                condition=models.Q(('product__isnull', False)),
                fields=('order', 'product'),
                name='unique_product_per_order',
            ),
        ),
    ]
