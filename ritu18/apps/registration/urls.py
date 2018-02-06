from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView

from ritu18.apps.registration.views import PaymentRequestAccept

urlpatterns = [
    path('', TemplateView.as_view(template_name='registration/payment.html'), name='index'),
    path('pay', PaymentRequestAccept.as_view(), name='pay'),
    path('sucess', TemplateView.as_view(template_name='registration/sucess.html'), name='sucess'),
    path('failure', TemplateView.as_view(template_name='registration/Failure.html'), name='failure')
]
