from decimal import Decimal

from django.test import TestCase

from .models import Category, Product


class ProductModelTests(TestCase):
    def test_product_stock_status(self):
        category = Category.objects.create(name='Phones')
        product = Product.objects.create(
            category=category,
            name='Phone',
            price=Decimal('100.00'),
            stock=2,
        )

        self.assertTrue(product.is_in_stock)

    def test_category_pages_use_database_categories(self):
        category = Category.objects.create(
            name='Accessories',
            description='Useful accessories',
        )

        list_response = self.client.get('/products/categories/')
        detail_response = self.client.get(
            f'/products/categories/{category.pk}/',
        )
        home_response = self.client.get('/')

        self.assertContains(list_response, 'Accessories')
        self.assertContains(detail_response, 'Useful accessories')
        self.assertContains(home_response, 'Accessories')

    def test_product_list_api_returns_active_products(self):
        category = Category.objects.create(name='API category')
        Product.objects.create(
            category=category,
            name='Visible product',
            price=Decimal('25.00'),
            is_active=True,
        )
        Product.objects.create(
            category=category,
            name='Hidden product',
            price=Decimal('30.00'),
            is_active=False,
        )

        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Visible product')

    def test_product_api_full_crud(self):
        category = Category.objects.create(name='CRUD category')

        create_response = self.client.post(
            '/api/products/',
            data={
                'category': category.id,
                'name': 'CRUD product',
                'sku': 'CRUD-001',
                'description': 'Initial description',
                'price': '100.00',
                'stock': 5,
                'is_active': True,
            },
        )
        self.assertEqual(create_response.status_code, 201)
        product_id = create_response.json()['id']

        list_response = self.client.get('/api/products/')
        detail_response = self.client.get(f'/api/products/{product_id}/')
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()['name'], 'CRUD product')

        update_response = self.client.patch(
            f'/api/products/{product_id}/',
            data={'price': '125.00', 'stock': 8},
            content_type='application/json',
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()['price'], '125.00')

        delete_response = self.client.delete(f'/api/products/{product_id}/')
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Product.objects.filter(id=product_id).exists())
