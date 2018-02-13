from django.contrib import admin

# Register your models here.
from django.contrib.admin import SimpleListFilter

from ritu18.apps.common.models import Profile
from ritu18.apps.registration.models import TransactionModel, RegistrationModel


class CategoryListFilter(SimpleListFilter):
    # USAGE
    # In your admin class, pass trhe filter class as tuple for the list_filter attribute:
    #
    # list_filter = (CategoryListFilter,)
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Payment Status'
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
            Returns a list of tuples. The first element in each
            tuple is the coded value for the option that will
            appear in the URL query. The second element is the
            human-readable name for the option that will appear
            in the right sidebar.
            """
        list_tuple = []
        for category in TransactionModel.TransactionStatus.STATUS_DESCRIPTION:
            # print category
            list_tuple.append((category, TransactionModel.TransactionStatus.STATUS_DESCRIPTION[category]))
        return list_tuple

    def queryset(self, request, queryset):
        """
            Returns the filtered queryset based on the value
            provided in the query string and retrievable via
            `self.value()`.
            """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value():
            return queryset.filter(status=self.value())
        else:
            return queryset


class RegistrationAdmin(admin.StackedInline):
    model = RegistrationModel


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['product_info', 'phone', 'email']
    list_filter = ['product_info', CategoryListFilter]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [RegistrationAdmin]
    search_fields = ['event_code']
