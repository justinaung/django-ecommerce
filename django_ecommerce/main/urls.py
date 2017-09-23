from django.conf.urls import url

from django_ecommerce.main import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^report$', views.report, name='report'),
]
