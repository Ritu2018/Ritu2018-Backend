import hashlib
from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.views import View

from config import MERCHANT_KEY, SALT, HTTP_AUTH, PAYU_URL, WEBSITE_URL
from ritu18.apps.registration.forms import PaymentRequestForm
from ritu18.apps.registration.models import TransactionModel, RegistrationModel
from ritu18.apps.event_details import event_details, AMOUNT


class PaymentRequestAccept(View):
    def post(self, request):
        if RegistrationModel.objects.filter(email=request.POST['phone'],
                                            event_code=request.POST['product_info']).exists():
            return JsonResponse({'status':'Already Registered'}) # TODO change to refirect URL
        try:
            if request.POST['product_info'] not in event_details:
                return JsonResponse({'status': 'Invalid Event Code'})
            transaction = TransactionModel(phone=request.POST['phone'],
                                           email=request.POST['email'],
                                           amount=event_details[request.POST['product_info']]['amount'],
                                           product_info=request.POST['product_info'],
                                           name=request.POST['name'])
            transaction.save()
            hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
            data = {
                'key': MERCHANT_KEY,
                'txnid': transaction.id,
                'amount': transaction.amount,
                'productinfo': transaction.product_info,
                'firstname': transaction.name,
                'email': transaction.email,
                'phone': transaction.phone,
                'surl': WEBSITE_URL + reverse('paymentResponse'),
                'furl': WEBSITE_URL + reverse('paymentResponse'),
                'service_provider': 'payu_paisa',
            }
            transaction_hash = "|".join([str(data.get(i, "")) for i in hashSequence.split("|")])
            transaction_hash = hashlib.sha512((transaction_hash + "|" + SALT).encode()).hexdigest().lower()
            data['hash'] = transaction_hash
            form = PaymentRequestForm(data=data)
            context = {
                'form': form,
                'header_auth': HTTP_AUTH,
                'url': PAYU_URL
            }
            request.META['AUTHORIZATION'] = HTTP_AUTH
            return render(request, 'registration/make_payment_request.html', context)
        except Exception as e:
            print(e)
        return JsonResponse({'status': 'fail'})  # TODO redirect to host website. Define the URL later into config.


@csrf_exempt
def payment_sucess(request):
    hash_sequence = 'salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key'

    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]

    retHashSeq = SALT + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hash = hashlib.sha512(retHashSeq.encode()).hexdigest().lower()

    if posted_hash != hash:
        return JsonResponse({'status': 'invalid'})

    transaction = TransactionModel.objects.get(id=txnid)
    status = request.POST['status']
    if status == 'success':
        if productinfo not in event_details:
            transaction.status = TransactionModel.PaymentStatus.INVALID_EVENT_CODE
        elif Decimal(amount) != Decimal(event_details[productinfo][AMOUNT]):
            print(amount)
            print(event_details[productinfo][AMOUNT])
            transaction.status = TransactionModel.PaymentStatus.INCORRECT_AMOUNT
        else:
            transaction.status = TransactionModel.PaymentStatus.SUCCESS
    else:
        transaction.status = TransactionModel.PaymentStatus.FAILURE

    transaction.payment_id = request.POST['payuMoneyId']
    transaction.save()

    if transaction.status == TransactionModel.PaymentStatus.SUCCESS:
        registration = RegistrationModel()
        registration.transaction = transaction
        registration.phone = transaction.phone
        registration.email = email
        registration.event_code = productinfo
        registration.save()

    return JsonResponse({'status': TransactionModel.PaymentStatus.STATUS_DESCRIPTION[transaction.status]}) #TODO change to Redirect URL


def registration_details(request):
    data = request.GET.get('data', "") #type:str
    rlist = None

    if '@' in data:
        rlist = RegistrationModel.objects.filter(email=data)
    else:
        rlist = RegistrationModel.objects.filter(phone=data)

    return JsonResponse({'list':[i.event_code for i in rlist]})