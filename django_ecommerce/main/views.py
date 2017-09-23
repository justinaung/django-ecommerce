from django.shortcuts import render

from django_ecommerce.main.models import StatusReport
from django_ecommerce.payments.models import User


def index(request):
    uid = request.session.get('user')
    if uid is None:
        return render(request, 'main/home.html')
    else:
        status = StatusReport.objects.latest()
        return render(
            request,
            'main/user.html',
            {'logged_in_user': User.get_by_id(uid), 'reports': status},
        )


def report(request):
    if request.method == 'POST':
        status = request.POST.get('status', '')

        if status:
            uid = request.session.get('user')
            user = User.get_by_id(uid)
            StatusReport.objects.create(user=user, status=status)

        return index(request)
