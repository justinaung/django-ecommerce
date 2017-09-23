from rest_framework import serializers

from django_ecommerce.main.models import StatusReport


class StatusReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusReport
        fields = ('id', 'user', 'when', 'status')

    def get_user(self, obj):
        return obj.user.email
