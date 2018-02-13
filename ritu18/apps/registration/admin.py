from django.contrib import admin

# Register your models here.
from ritu18.apps.common.models import Profile
from ritu18.apps.registration.models import TransactionModel, RegistrationModel

class RegistrationAdmin(admin.StackedInline):
    model = RegistrationModel

@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['product_info', 'phone']
    list_filter = ['product_info', 'phone']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [RegistrationAdmin]
    search_fields = ['event_code']
