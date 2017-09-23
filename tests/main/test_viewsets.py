from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django_ecommerce.main.api.serializers import StatusReportSerializer
from django_ecommerce.main.models import StatusReport
from django_ecommerce.payments.models import User


class StatusReportViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(name='test', email='test@test.com')
        self.user2 = User.objects.create(name='test2', email='test2@test.com')

        self.status = StatusReport.objects.create(
            user=self.user, status='hello world'
        )
        self.status2 = StatusReport.objects.create(
            user=self.user2, status='hello world'
        )


    def test_get_status_reports(self):
        status = StatusReport.objects.all()
        expected_json = StatusReportSerializer(status, many=True).data

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('api:status-reports-list'))

        self.assertEqual(expected_json, response.data)

    def test_get_status_reports_requires_logged_in_user(self):
        response = self.client.get(reverse('api:status-reports-list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
