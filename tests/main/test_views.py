from unittest import mock

import re
from django.shortcuts import render_to_response
from django.test import TestCase, RequestFactory
from django.urls import resolve

from django_ecommerce.main.models import StatusReport
from django_ecommerce.main.views import index


class MainPageTests(TestCase):

    #############
    #   Setup   #
    #############
    def setUp(self):
        request_factory = RequestFactory()
        self.request = request_factory.get('/')
        self.request.session = dict()

    ######################
    #   Testing routes   #
    ######################

    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    def test_retuns_appropriate_html_response_code(self):
        resp = index(self.request)
        self.assertEqual(resp.status_code, 200)

    ###################################
    #   Testing templates and views   #
    ###################################

    def test_returns_exact_html(self):
        home = self.client.get('/')
        self.assertEqual(home.content, 
                         render_to_response('main/home.html').content)

    def test_index_handles_logged_in_user(self):
        # create a dummy request
        self.request.session['user'] = 1

        with mock.patch('django_ecommerce.main.views.User') as user_mock:
            # tell the mock what to do when called
            config = {'get.return_value': mock.Mock()}
            user_mock.objects.configure_mock(**config)

            # request the index page
            resp = index(self.request)
            # verify it returns the page for the logged-in user
            status = StatusReport.objects.latest()
            expected_html = render_to_response(
                'main/user.html',
                {'logged_in_user': user_mock.get_by_id(1),
                 'reports': status},
            )
            self.assertEqual(self.remove_csrf(resp.content.decode()),
                             expected_html.content.decode())

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)
