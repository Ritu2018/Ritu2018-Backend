import hashlib

from django.shortcuts import render
# Create your views here.
from django.views import View

from config import MERCHANT_KEY, SALT, HTTP_AUTH, PAYU_URL
from ritu18.apps.registration.forms import PaymentRequestForm
from ritu18.apps.registration.models import TransactionModel


class PaymentRequestAccept(View):

    def post(self,request):
        transaction = TransactionModel(phone=request.POST['phone'],
                                       email=request.POST['email'],
                                       amount=request.POST['amount'],
                                       product_info=request.POST['product_info'],
                                       name= request.POST['name'])
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
            'surl': 'localhost:8000/sucess',
            'furl': 'localhost:8000/failure',
            'service_provider': 'payu_paisa',
        }
        transaction_hash = "|".join([str(data.get(i,"")) for i in hashSequence.split("|")])
        print(transaction_hash)
        transaction_hash = hashlib.sha512((transaction_hash+"|"+SALT).encode()).hexdigest().lower()
        data['hash'] = transaction_hash
        #pay_request = requests.post(headers={'authorization':HTTP_AUTH}, data=data, url=PAYU_URL)
        form = PaymentRequestForm(data=data)
        print(form.as_p(), data)
        print(PaymentRequestForm())
        context = {
            'form': form,
            'header_auth': HTTP_AUTH,
            'url': PAYU_URL
        }
        request.META['AUTHORIZATION'] = HTTP_AUTH
        return render(request,'registration/make_payment_request.html',context)