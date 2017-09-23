from collections import OrderedDict

from django.test import TestCase
from io import BytesIO

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from django_ecommerce.main.api.serializers import StatusReportSerializer
from django_ecommerce.main.models import StatusReport
from django_ecommerce.payments.models import User


class StatusReportSerializerTests(TestCase):
    def setUp(self):
        self.user = User(name='test', email='test@test.com')
        self.user.save()

        self.new_status = StatusReport(user=self.user, status='hello world')
        self.new_status.save()

        when = self.new_status.when.isoformat()
        if when.endswith('+00:00'):
            when = when[:-6] + 'Z'

        self.expected_dict = {
            'id': self.new_status.id,
            'user': self.user.id,
            'when': when,
            'status': 'hello world'
        }

    def test_model_to_dictionary(self):
        serializer = StatusReportSerializer(self.new_status)
        self.assertDictEqual(self.expected_dict, serializer.data)

    def test_dictionary_to_json(self):
        serializer = StatusReportSerializer(self.new_status)
        content = JSONRenderer().render(serializer.data)
        expected_json = JSONRenderer().render(self.expected_dict)
        self.assertEqual(expected_json, content)

    def test_json_to_update_object(self):
        json = JSONRenderer().render(self.expected_dict)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)

        serializer = StatusReportSerializer(self.new_status, data=data)
        self.assertTrue(serializer.is_valid())

        status = serializer.save()
        self.assertEqual(self.new_status.id, status.id)
        self.assertEqual(self.new_status.status, status.status)
        self.assertEqual(self.new_status.when, status.when)
        self.assertEqual(self.new_status.user, status.user)

    def test_json_to_create_object(self):
        json = JSONRenderer().render(self.expected_dict)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)

        serializer = StatusReportSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        status = serializer.save()
        self.assertEqual(self.new_status.status, status.status)
        self.assertIsNotNone(status.when)
        self.assertEqual(self.new_status.user, status.user)
