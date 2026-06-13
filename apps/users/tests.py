from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import CustomerProfile


class CustomerProfileModelTests(TestCase):
    def test_profile_string_uses_username(self):
        user = get_user_model().objects.create_user(username='customer')
        profile = CustomerProfile.objects.create(user=user)

        self.assertEqual(str(profile), 'customer')
