from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from applications.payments.models import Payment, UserPayment, PropertyPayment
from applications.property.serializers import PropertyListSerializer


class PropertyPaymentSerializer(serializers.ModelSerializer):

    """
    Serializer for payment tracking.
    """

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyPayment
        fields = ("billing_address",)




class UserPaymentPaymentSerializer(serializers.ModelSerializer):

    """
    Serializer for user payment tracking.
    """

    class Meta:
        model = UserPayment
        fields = "__all__"
