from django.db import models


class StatusReportQuerySet(models.QuerySet):
    def latest(self):
        return self.all().order_by('-when')[:20]


class StatusReport(models.Model):
    user = models.ForeignKey('payments.User')
    when = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200)

    objects = StatusReportQuerySet.as_manager()
