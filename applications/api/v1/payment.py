import datetime as dt

from django.conf import settings
from django.http import Http404
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from utils.helpers import ErrorType

from applications.property.models import Property
from applications.accounts.models import User
from applications.agent.models import Agent
from applications.builder.models import Builder
from applications.payments.models import PropertyPayment
from applications.payments.serializer import (
    PropertyPaymentSerializer,
    UserPaymentPaymentSerializer,
    PaymentSerializer,
)
from applications.payments.utils import generate_order_id, enc_request, dec_response
from applications.payments import POST_URL
from utils.constants import *


class PaymentExecuteView(APIView, ErrorType):

    serializer_class = PropertyPaymentSerializer
    # save the payment created by agent, builder and each property

    def post(self, request, format=None):
        billing_address = request.data.get("billing_address")
        property_id = request.data.get("property_id")#if payment  is for property
        user = request.data.get("user_id")#if payment  is for user
        today = dt.datetime.today().strftime("%Y-%m-%d")
        status = request.data.get("status")
        if status=="success":
            if property_id:
                try:
                    property = Property.objects.get(id=property_id)
                    property.is_premium = True
                    property.payment_created = today
                    property.save()
                    payment_property, created = PropertyPayment.objects.get_or_create(property=property, billing_address=billing_address)
                    data = request.POST.copy()
                    data.update({'payment_property': payment_property.id})
                except Property.DoesNotExist:
                    raise Http404
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                return Response({"payment-redirect": True})
            if user:
                user = User.objects.get(id=user)
                if user.type == AGENT:
                    try:
                        payment_user = Agent.objects.get(user_agent=user)
                    except Agent.DoesNotExist:
                        raise Http404
                if user.type == BUILDER:
                    try:
                        payment_user = Builder.objects.get(user_builder=user)
                    except Builder.DoesNotExist:
                        raise Http404
                payment_user.premium = True
                payment_user.payment_created = today
                payment_user.save()
                data = request.POST.copy()
                data.update({'user':user.id})
                serializer_class = UserPaymentPaymentSerializer
                serializer = serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                return Response({"payment-redirect": True})
        else:
            if property_id:
                property = Property.objects.get(id=property_id)
                payment_property, created = PropertyPayment.objects.get_or_create(property=property, billing_address=billing_address)
                data = request.POST.copy()
                data.update({'payment_property':payment_property.id})
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
            if user:
                user = User.objects.get(id=user)
                data = request.POST.copy()
                data.update({'user': user.id})
                serializer_class = UserPaymentPaymentSerializer
                serializer = serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
            return Response({"payment-redirect": False})


class PaymentStartView(APIView, ErrorType):

    def get(self, request, format=None):
        serializer_class = PaymentSerializer
        property_id = request.GET.get("property_id")#get billing address if already saved
        if property_id:
            property = Property.objects.get(id=property_id)
            properties = PropertyPayment.objects.filter(property=property)
            if properties:
                serializer = serializer_class(properties, many=True)
                return Response(serializer.data)
        else:
            raise Http404

    def post(self, request, format=None):
        order_id = request.GET.get("Order_Id")
        if not order_id:
            order_id = generate_order_id()
        enc_request_data = enc_request(request, order_id=order_id)
        request.session["dcavenue_order_id"] = order_id

        return Response(
            """
                <html>
                    <head><title>Redirecting...</title></head>
                    <body>
                        <form method="post" name="redirect" action="%s">
                        <input type="" name="command" value="%s">
                        <input type="hidden" name="merchant_id" value="%s">
                        <input type="hidden" name="encRequest" value="%s">
                        <input type="hidden" name="access_code" value="%s">
                        </form>
                    </body>
                    <script language='javascript'>
                        document.redirect.submit();
                    </script>
                </html>
            """ % (POST_URL, 'initiateTransaction&',settings.MERCHANT_ID, enc_request_data,settings.ACCESS_CODE, )
        )