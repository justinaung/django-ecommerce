from django.shortcuts import render

from django_ecommerce.payments.models import User


def index(request):
    uid = request.session.get('user')
    if uid is None:
        return render(request, 'home.html')
    else:
        return render(request, 'user.html', {'logged_in_user': User.objects.get(pk=uid)})
