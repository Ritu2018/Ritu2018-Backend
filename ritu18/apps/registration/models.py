from django.db import models


# Create your models here.

class TransactionModel(models.Model):
    class PaymentStatus:
        SUCCESS = 's'
        FAILURE = 'f'
        ERROR = 'e'
        INCORRECT_AMOUNT = 'i'
        INVALID_EVENT_CODE = 'h'

        STATUS_DESCRIPTION = {
            SUCCESS:'Success',
            FAILURE:'Failure',
            ERROR: 'Transaction Error',
            INCORRECT_AMOUNT: 'Incorrect Amount',
            INVALID_EVENT_CODE: 'Invalid Event Code'

        }

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    email = models.EmailField()
    product_info = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=1, default=PaymentStatus.ERROR)

    payment_id = models.CharField(max_length=50,null=True)


class RegistrationModel(models.Model):
    event_code = models.CharField(max_length=10)

    email = models.EmailField()
    phone = models.CharField(max_length=14)

    transaction = models.OneToOneField(TransactionModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('phone','event_code'))

