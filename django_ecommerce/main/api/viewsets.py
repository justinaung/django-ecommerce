from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from django_ecommerce.main.api.permissions import IsOwnerOrReadOnly
from django_ecommerce.main.api.serializers import StatusReportSerializer
from django_ecommerce.main.models import StatusReport


class StatusReportViewSet(ModelViewSet):
    queryset = StatusReport.objects.all()
    serializer_class = StatusReportSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
