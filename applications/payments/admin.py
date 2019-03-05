from django.contrib import admin

from applications.payments.models import Payment, PropertyPayment, UserPayment

admin.site.register(Payment)
admin.site.register(PropertyPayment)
admin.site.register(UserPayment)