from django.conf.urls import include, url
from django.urls import path
from django.views.generic import TemplateView

from ritu18.apps.registration.views import PaymentRequestAccept, payment_sucess, registration_details

urlpatterns = [
    path('pay', PaymentRequestAccept.as_view(), name='pay'),
    path('pay/response', payment_sucess, name='paymentResponse'),
    path('get/registration', registration_details, name='getRegistrationDetails' ),
    path('', TemplateView.as_view(template_name='registration/index.html'), name='index'),
]
