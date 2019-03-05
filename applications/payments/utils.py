import random
import uuid
import zlib
import subprocess
from pprint import pformat

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from applications.payments.ccavutil import encrypt


def generate_order_id():
    return uuid.uuid4().hex


def get_redirect_url(request):
    url = settings.DOMAIN +"/#/"
    if request.is_secure():
        return "http://%s" % (url, )
    else:
        return "http://%s" % (url, )


def checksum(redirect_url, amount, order_id):
    # "$MerchantId|$OrderId|$Amount|$redirectUrl|$WorkingKey"

    data = "%s|%s|%s|%s|%s" % (
        settings.MERCHANT_ID, order_id, amount,
        redirect_url, settings.WORKING_KEY
    )
    csum = zlib.adler32(data.encode(), 1)
    if csum < 0:
        csum += 2 ** 32

    return csum


def enc_request(request, order_id):
    amount = request.GET["Amount"]
    billing_address = request.GET["billing_address"]
    redirect_url = get_redirect_url(request)+"add/"
    cancel_url = get_redirect_url(request)+"login/"
    merchant_data = 'merchant_id=' + settings.MERCHANT_ID + '&' + 'order_id=' + order_id + '&' + 'amount=' + amount + '&' + \
                    'redirect_url=' + redirect_url + '&' + 'cancel_url=' + cancel_url + '&' + 'billing_address=' + billing_address + '&'+'currency=INR'+'&'
    encryption = encrypt(merchant_data, settings.WORKING_KEY)
    return encryption


#noinspection PyTypeChecker
def verify_checksum(data):
    # "$MerchantId|$OrderId|$Amount|$AuthDesc|$WorkingKey";
    inp = "%s|%s|%s|%s|%s" % (
        settings.MERCHANT_ID, data["Order_Id"], data["Amount"],
        data["AuthDesc"], settings.WORKING_KEY
    )

    csum = zlib.adler32(inp, 1)

    if csum < 0:
        csum += 2 ** 32

    return str(csum) == data['Checksum']


def dec_response(request, response):
    response = subprocess.getoutput(
        '%s -jar %s %s "%s" dec' % (
            settings.DCAVENUE.get("JAVA", "java"), settings.DCAVENUE["JAR"],
            settings.WORKING_KEY, response
        )
    )

    data = dict(
        part.split("=", 1) for part in response.split("&")
    )

    if not verify_checksum(data):
        return None

    return data


def default_callback(request, data):
    return HttpResponse(
        """
            <html>
                <body>
                    %s
                </body>
            </html>
        """ % pformat(data)
    )