from rest_framework.viewsets import ModelViewSet

from django_ecommerce.main.api.serializers import StatusReportSerializer
from django_ecommerce.main.models import StatusReport


class StatusReportViewSet(ModelViewSet):
    queryset = StatusReport.objects.all()
    serializer_class = StatusReportSerializer
