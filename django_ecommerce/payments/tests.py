from pprint import pformat
from unittest import skip, mock

from django import forms
from django.conf import settings
from django.shortcuts import render_to_response
from django.test import TestCase, SimpleTestCase, RequestFactory
from django.urls import resolve

from django_ecommerce.payments.forms import SigninForm, UserForm, CardForm
from django_ecommerce.payments.models import User
from django_ecommerce.payments.views import sign_in, soon, register


class UserModelTest(TestCase):

    def setUp(self):
        self.test_user = User(email='j@j.com', name='test user')
        self.test_user.save()

    def test_user_to_string_print_email(self):
        self.assertEqual(str(self.test_user), 'j@j.com')

    def test_get_by_id(self):
        self.assertEqual(User.get_by_id(1), self.test_user)


class FormTesterMixin:

    def assertCustomFormError(self, form_cls, expected_error_name,
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


class ViewTesterMixin:

    @classmethod
    def setupViewTester(cls, url, view_func, expected_html, status_code=200,
                        session=None):
        request_factory = RequestFactory()
        cls.request = request_factory.get(url)
        cls.request.session = session or dict()
        cls.status_code = status_code
        cls.url = url
        cls.view_func = staticmethod(view_func)
        cls.expected_html = expected_html

    def test_resolves_to_correct_view(self):
        test_view = resolve(self.url)
        self.assertEqual(test_view.func, self.view_func)

    def test_returns_appropriate_response_code(self):
        resp = self.view_func(self.request)
        self.assertEqual(resp.status_code, self.status_code)

    @skip
    def test_returns_correct_html(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.content, self.expected_html)


class SignInPageTests(ViewTesterMixin, SimpleTestCase):

    def setUp(self):
        html = render_to_response(
            'sign_in.html',
            {
                'form': SigninForm(),
                'user': None
            }
        )
        ViewTesterMixin.setupViewTester('/sign_in/', sign_in, html.content)


class FormTests(FormTesterMixin, SimpleTestCase):

    def test_signin_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': {'email': 'j@j.com'},
             'error': ('password', [u'This field is required.'])},
            {'data': {'password': '1234'},
             'error': ('email', [u'This field is required.'])}
        ]

        for invalid_data in invalid_data_list:
            self.assertCustomFormError(SigninForm,
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

    def test_card_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {
                'data': {'last_4_digits': '123'},
                'error': (
                    'last_4_digits',
                    [u'Ensure this value has at least 4 characters (it has 3).']
                )
            },
            {
                'data': {'last_4_digits': '12345'},
                'error': (
                    'last_4_digits',
                    [u'Ensure this value has at most 4 characters (it has 5).']
                )
            }
        ]

        for invalid_data in invalid_data_list:
            self.assertCustomFormError(
                CardForm,
                invalid_data['error'][0],
                invalid_data['error'][1],
                invalid_data['data']
            )


class RegisteredPageTests(ViewTesterMixin, TestCase):

    def setUp(self):
        html = render_to_response(
            'register.html',
            {
                'form': UserForm(),
                'months': range(1, 13),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': range(2011, 2036),
            }
        )
        ViewTesterMixin.setupViewTester(
            '/register/',
            register,
           html.content
        )

    def test_invalid_form_returns_registration_page(self):
        with mock.patch('django_ecommerce.payments.forms.UserForm.is_valid') as user_mock:
            user_mock.return_value = False

            resp = self.client.post('/register/')
            self.assertContains(resp, 'Register Today')

            # make sure that we did indeed call our is_valid function
            self.assertEqual(user_mock.call_count, 1)

    @skip
    def test_registering_new_user_returns_successfully(self):
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'justin@loverant.com',
            'name': 'Justin',
            'stripe_token': '...',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password'
        }
        with mock.patch('stripe.Customer') as stripe_mock:
            config = {'create.return_value': mock.Mock()}
            stripe_mock.configure_mock(**config)

            resp = register(self.request)

            self.assertEqual(resp.content, "")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.session['user'], 1)

            User.objects.get(email='justin@loverant.com')
