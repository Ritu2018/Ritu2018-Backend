from django import forms


class PaymentRequestForm(forms.Form):
    """
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
    """
    key = forms.CharField(widget=forms.HiddenInput())
    txnid = forms.CharField(widget=forms.HiddenInput())
    amount = forms.CharField(widget=forms.HiddenInput())
    productinfo = forms.CharField(widget=forms.HiddenInput())
    firstname = forms.CharField(widget=forms.HiddenInput())
    email = forms.CharField(widget=forms.HiddenInput())
    phone = forms.CharField(widget=forms.HiddenInput())
    surl = forms.CharField(widget=forms.HiddenInput())
    furl = forms.CharField(widget=forms.HiddenInput())
    service_provider = forms.CharField(widget=forms.HiddenInput())
    hash = forms.CharField(widget=forms.HiddenInput())
