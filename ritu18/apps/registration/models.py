from django.db import models, IntegrityError

# Create your models here.
from ritu18.apps.common.models import Profile


class TransactionModel(models.Model):
    class TransactionStatus:
        SUCCESS = 's'
        FAILURE = 'f'
        ERROR = 'e'
        INCORRECT_AMOUNT = 'i'
        INVALID_EVENT_CODE = 'h'
        REPEATED_REGISTRATION = 'r'
        PAYMENT_PENDING = 'p'

        STATUS_DESCRIPTION = {
            SUCCESS: 'Success',
            FAILURE: 'Failure',
            ERROR: 'Transaction Error',
            INCORRECT_AMOUNT: 'Incorrect Amount',
            INVALID_EVENT_CODE: 'Invalid Event Code',
            REPEATED_REGISTRATION: 'Repeated Registration',
            PAYMENT_PENDING: 'Payment Pending'

        }

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    email = models.EmailField()
    product_info = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=1, default=TransactionStatus.PAYMENT_PENDING)

    payment_id = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name + " : " + self.phone + " : " + self.product_info + "|amount: " + str(self.amount) \
               + "|status:" +self.TransactionStatus.STATUS_DESCRIPTION[self.status]


class RegistrationModel(models.Model):
    event_code = models.CharField(max_length=10)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    transaction = models.OneToOneField(TransactionModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.event_code

    class Meta:
        unique_together = (('profile', 'event_code'),)

    class RepeatedRegistrationException(Exception):
        pass

    @classmethod
    def create_registration(cls, name: str, phone: str, email: str, transaction: TransactionModel):
        profile, created = Profile.objects.get_or_create(name=name, phone=phone, email=email)  # type:Profile
        registration = RegistrationModel(event_code=transaction.product_info, profile=profile, transaction=transaction)
        try:
            registration.save()
        except IntegrityError:
            raise RegistrationModel.RepeatedRegistrationException(profile.email + ' already registered for event.')
        return registration
