from django.shortcuts import render_to_response
from django.test import TestCase
from django.urls import reverse

from django_ecommerce.contact.models import ContactForm
from django_ecommerce.contact.views import contact
from django_ecommerce.payments.tests import ViewTesterMixin


class ContactPageTest(ViewTesterMixin, TestCase):

    def setUp(self):
        html = render_to_response(
            'contact.html',
            {
                'form': ContactForm(),
                'user': None
            }
        )
        ViewTesterMixin.setupViewTester('/contact/', contact, html.content)


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
        resp = self.client.post(reverse('contact'), data=data, follow=True)
        self.assertContains(resp, 'Your message has been sent. Thank you.')
