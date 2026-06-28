from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    def test_create_user_with_phone_number(self):
        User = get_user_model()
        user = User.objects.create_user(phone_number='+998901234567', password='password123')
        self.assertEqual(user.phone_number, '+998901234567')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), '+998901234567')

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(phone_number='+998901234567', password='password123')
        self.assertEqual(superuser.phone_number, '+998901234567')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_phone_number_raises_error(self):
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(phone_number='', password='password123')


class UserAuthenticationTests(TestCase):
    def test_login_page_renders(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_post_authenticates_user(self):
        User = get_user_model()
        user = User.objects.create_user(phone_number='+998901234567', password='password123')
        
        response = self.client.post('/users/login/', {
            'phone_number': '+998901234567',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home
        
    def test_signup_post_creates_user(self):
        response = self.client.post('/users/signup/', {
            'phone_number': '+998909876543',
            'first_name': 'Sherzod',
            'last_name': 'Aliyev',
            'password': 'password456'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home
        User = get_user_model()
        self.assertTrue(User.objects.filter(phone_number='+998909876543').exists())

    def test_logout_redirects(self):
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)  # Redirects to home
