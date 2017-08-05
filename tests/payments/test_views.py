import socket

from unittest import skip, mock

from django.conf import settings
from django.shortcuts import render_to_response
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import resolve

from django_ecommerce.payments.forms import SigninForm, UserForm
from django_ecommerce.payments.models import User
from django_ecommerce.payments.views import sign_in, soon, register


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
        with mock.patch(
            'django_ecommerce.payments.forms.UserForm.is_valid'
        ) as user_mock:
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

    def test_registering_user_when_stripe_is_down(self):
        # create the request used to test the view
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'python@rocks.com',
            'name': 'pyRock',
            'stripe_token': '...',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password',
        }

        # mock out Stripe and ask it to throw a connection error
        with mock.patch(
            'stripe.Customer.create',
            side_effect=socket.error("Can't connect to Stripe")
        ):
            # run the test
            register(self.request)

            # assert there is a record in the database without Stripe id.
            users = User.objects.filter(email='python@rocks.com')
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0].stripe_id, '')
