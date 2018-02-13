import hashlib
from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.views import View

from config import MERCHANT_KEY, SALT, HTTP_AUTH, PAYU_URL, WEBSITE_URL
from ritu18.apps.registration.forms import PaymentRequestForm
from ritu18.apps.registration.models import TransactionModel, RegistrationModel
from ritu18.apps.event_details import event_details, AMOUNT


class PaymentRequestAccept(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentRequestAccept, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        phone = request.POST['phone']
        product_info = request.POST['product_info']
        if RegistrationModel.objects.filter(profile__phone=phone, event_code=product_info).exists():
            return JsonResponse({'status':'Repeated Registration'}) #TODO change
        try:
            if request.POST['product_info'] not in event_details:
                return JsonResponse({'status': 'Invalid Event Code'}) #TODO change
            transaction = TransactionModel(phone=request.POST['phone'],
                                           email=request.POST['email'],
                                           amount=event_details[request.POST['product_info']]['amount'],
                                           product_info=request.POST['product_info'],
                                           name=request.POST['name'])
            transaction.save()
            transaction.transaction_id = 'TEST00' + str(transaction.id)
            transaction.save()

            hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
            data = {
                'key': MERCHANT_KEY,
                'txnid': transaction.transaction_id,
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
        return JsonResponse({'status': 'invalid'}) # TODO change

    transaction = TransactionModel.objects.get(id=txnid)
    status = request.POST['status']
    if status == 'success':
        if productinfo not in event_details:
            transaction.status = TransactionModel.TransactionStatus.INVALID_EVENT_CODE
        elif Decimal(amount) != Decimal(event_details[productinfo][AMOUNT]):
            transaction.status = TransactionModel.TransactionStatus.INCORRECT_AMOUNT
        else:
            transaction.status = TransactionModel.TransactionStatus.SUCCESS
    else:
        transaction.status = TransactionModel.TransactionStatus.FAILURE

    transaction.payment_id = request.POST['payuMoneyId']
    transaction.save()

    if transaction.status == TransactionModel.TransactionStatus.SUCCESS:
        try:
            registration = RegistrationModel.create_registration(name=transaction.name,
                                                                 phone=transaction.phone,
                                                                 email=transaction.email,
                                                                 transaction=transaction)  # type: RegistrationModel
        except RegistrationModel.RepeatedRegistrationException:
            transaction.status = TransactionModel.TransactionStatus.REPEATED_REGISTRATION
            transaction.save()
            return JsonResponse({'status': 'fail'}) # TODO change
    return JsonResponse({'status': TransactionModel.TransactionStatus.STATUS_DESCRIPTION[transaction.status]}) #TODO change to Redirect URL


def registration_details(request):
    data = request.GET.get('data', "")  # type:str
    rlist = None

    if '@' in data:
        rlist = RegistrationModel.objects.filter(email=data)
    else:
        rlist = RegistrationModel.objects.filter(phone=data)

    return JsonResponse({'list':[i.event_code for i in rlist]})