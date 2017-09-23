from django.test import TestCase

from django_ecommerce.payments.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.test_user = User(email='j@j.com', name='test user')
        self.test_user.save()

    def test_user_to_string_print_email(self):
        self.assertEqual(str(self.test_user), 'j@j.com')

    def test_get_by_id(self):
        self.assertEqual(User.get_by_id(self.test_user.id), self.test_user)
