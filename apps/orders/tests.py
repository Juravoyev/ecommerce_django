from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.products.models import Category, Product
from .models import Order, OrderItem


class OrderModelTests(TestCase):
    def test_item_copies_product_data_and_order_calculates_total(self):
        user = get_user_model().objects.create_user(username='customer')
        category = Category.objects.create(name='Laptops')
        product = Product.objects.create(
            category=category,
            name='Laptop',
            price=Decimal('750.00'),
            stock=5,
        )
        order = Order.objects.create(user=user, address='Tashkent')
        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
        )

        self.assertEqual(item.product_name, 'Laptop')
        self.assertEqual(item.unit_price, Decimal('750.00'))
        self.assertEqual(order.calculate_total(), Decimal('1500.00'))

    def test_order_list_api_returns_orders(self):
        user = get_user_model().objects.create_user(username='api-customer')
        order = Order.objects.create(
            user=user,
            full_name='API Customer',
            phone='+998901234567',
            address='Tashkent',
            total_price=Decimal('250.00'),
        )

        response = self.client.get('/api/orders/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], order.id)
        self.assertEqual(response.json()[0]['status'], Order.Status.PENDING)

    def test_order_patch_update_works_without_trailing_slash(self):
        user = get_user_model().objects.create_user(username='patch-customer')
        order = Order.objects.create(
            user=user,
            address='Old address',
        )

        response = self.client.patch(
            f'/api/orders/{order.id}/',
            data={'status': Order.Status.PROCESSING},
            content_type='application/json',
        )

        order.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(order.status, Order.Status.PROCESSING)

    def test_order_api_full_crud(self):
        user = get_user_model().objects.create_user(username='crud-customer')

        create_response = self.client.post(
            '/api/orders/',
            data={
                'user': user.id,
                'full_name': 'CRUD Customer',
                'phone': '+998901112233',
                'address': 'Tashkent',
            },
        )
        self.assertEqual(create_response.status_code, 201)
        order_id = create_response.json()['id']

        list_response = self.client.get('/api/orders/')
        detail_response = self.client.get(f'/api/orders/{order_id}/')
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()['full_name'], 'CRUD Customer')

        update_response = self.client.patch(
            f'/api/orders/{order_id}/',
            data={'status': Order.Status.SHIPPED},
            content_type='application/json',
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()['status'], Order.Status.SHIPPED)

        delete_response = self.client.delete(f'/api/orders/{order_id}/')
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Order.objects.filter(id=order_id).exists())
