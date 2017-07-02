from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from django_ecommerce.contact.views import contact


class ContactPageTest(TestCase):

    #############
    ### Setup ###
    #############
    def setUp(self):
        request_factory = RequestFactory()
        self.request = request_factory.get('/')
        self.request.session = dict()

    ######################
    ### Testing routes ###
    ######################

    def test_contact_route_returns_appropriate_code(self):
        resp = contact(self.request)
        self.assertEqual(resp.status_code, 200)

    ################################
    ### Testing sending messages ###
    ################################

    def test_message_submittion_should_work(self):
        data = {
            'name': 'jj',
            'email': 'j@j.com',
            'topic': 'testing',
            'message': 'testing 123'
        }
        c = Client()

        resp = c.post(reverse('contact'), data=data, follow=True)
        self.assertContains(resp, 'Your message has been sent. Thank you.')
