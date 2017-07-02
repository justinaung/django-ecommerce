from pprint import pformat

from django import forms
from django.test import TestCase, SimpleTestCase

from django_ecommerce.payments.forms import SigninForm, UserForm
from django_ecommerce.payments.models import User


class UserModelTest(TestCase):

    def setUp(self):
        self.test_user = User(email='j@j.com', name='test user')
        self.test_user.save()

    def test_user_to_string_print_email(self):
        self.assertEqual(str(self.test_user), 'j@j.com')

    def test_get_by_id(self):
        self.assertEqual(User.get_by_id(1), self.test_user)


class FormTesterMixin:

    def assertCustFormError(self: SimpleTestCase, form_cls, expected_error_name,
                        expected_error_msg, data):
        test_form = form_cls(data=data)

        # if we get an error then the form should not be valid
        self.assertFalse(test_form.is_valid())

        self.assertEquals(
            test_form.errors[expected_error_name],
            expected_error_msg,
            msg=f"Expected {test_form.errors[expected_error_name]} "
                f": Actual {expected_error_msg} : using data {pformat(data)}"
        )


class FormTests(SimpleTestCase, FormTesterMixin):

    def test_signin_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': {'email': 'j@j.com'},
             'error': ('password', [u'This field is required.'])},
            {'data': {'password': '1234'},
             'error': ('email', [u'This field is required.'])}
        ]

        for invalid_data in invalid_data_list:
            self.assertCustFormError(SigninForm,
                                     invalid_data['error'][0],
                                     invalid_data['error'][1],
                                     invalid_data['data'])

    def test_user_form_passwords_match(self):
        form = UserForm(
            {
                'name': 'jj',
                'email': 'j@j.com',
                'password': '1234',
                'ver_password': '1234',
                'last_4_digits': '3333',
                'stripe_token': '1',
            }
        )
        # is the data vaild? -- if not print out the errors
        self.assertTrue(form.is_valid(), form.errors)

        # this will throw an error if the form doesn't clean correctly
        self.assertIsNotNone(form.clean())


    def test_user_form_passwords_dont_match_throws_error(self):
        form = UserForm(
            {
                'name': 'jj',
                'email': 'j@j.com',
                'password': '234',
                'ver_password': '1234',  # bad password
                'last_4_digits': '3333',
                'stripe_token': '1'
            }
        )

        # is the data valid?
        self.assertFalse(form.is_valid())

        self.assertRaisesMessage(forms.ValidationError,
                                 'Passwords do not match')
