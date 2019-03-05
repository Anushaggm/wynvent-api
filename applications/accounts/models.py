from __future__ import unicode_literals
import requests
import hashlib
import json

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template import Context

from applications.property.models import Property
from applications.builder.models import Builder
from applications.agent.models import Agent
from applications.locations.models import City
from utils.helpers import send_user_register_email, get_new_avatar_path
from utils.constants import *
from utils.db import WynventPostgresDBBaseModel


class User(AbstractUser):
    """ Custom user model for User. """

    mobile = models.CharField(max_length=50)
    type = models.CharField(choices=USER_TYPES, max_length=25, default=BUYER_OWNER)
    profile_image = models.ImageField(upload_to=get_new_avatar_path, blank=True)
    about_me = models.TextField(blank=True)
    builder = models.ForeignKey(Builder, null=True, blank=True)
    agent = models.ForeignKey(Agent, null=True, blank=True)

    # Properties
    shortlisted_properties = models.ManyToManyField(
        Property, related_name="shortlisted_properties", blank=True)

    class Meta:
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.get_username()

    def get_full_name(self):
        if not self.last_name:
            return self.first_name
        return "%s %s" % (self.first_name, self.last_name)

    full_name = property(get_full_name)


def mailchimp_subscribe_user(sender, instance, created, **kwargs):
    if created:
        send_user_register_email(instance)
        url = settings.MAILCHIMP_API_ENDPOINT+'lists/%s/members' % settings.MAILCHIMP_LIST_ID
        try:
            email = instance.email
            fname = instance.first_name
            lname = instance.last_name

            data = {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": {
                    "FNAME": fname,
                    "LNAME": lname
                }
            }
            resp = requests.post(url, data=json.dumps(data),
                                 auth=(settings.MAILCHIMP_USERNAME, settings.MAILCHIMP_ACCESS_KEY))
        except Exception as e:
            print(e)


def mailchimp_delete_user(sender, instance, **kwargs):

    try:
        email = instance.email
        m = hashlib.md5()
        m.update(email.encode('utf-8'))
        email_md5 = m.hexdigest()
        url = settings.MAILCHIMP_API_ENDPOINT + 'lists/%s/members/%s/' % (
            settings.MAILCHIMP_LIST_ID, email_md5)
        resp = requests.delete(url, auth=(
            settings.MAILCHIMP_USERNAME, settings.MAILCHIMP_ACCESS_KEY))

    except Exception as e:
        print(e)


# post_save.connect(mailchimp_subscribe_user, sender=User)
post_delete.connect(mailchimp_delete_user, sender=User)


class ContactUs(WynventPostgresDBBaseModel):

    """ Contact us model """

    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), blank=True)
    message = models.TextField(blank=True)
    city = models.ForeignKey(City, null=True, blank=True)

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')

    def __str__(self):
        return self.name+'-'+self.email

@receiver(post_save, sender=ContactUs, dispatch_uid="post_save_contest_entry")
def contest_entry_signal(instance, **kwargs):
    #need to change from email and subject
    created = kwargs['created']

    if created:
        email = EmailMessage('Contact Us', instance.message, to=[settings.ADMIN_EMAIL])
        email.send()
        email.body = 'We have received your message.Thank You.'
        email.to = [instance.email, ]
        email.send()
    else:
        pass


class FeedBack(WynventPostgresDBBaseModel):

    """ Feedback model """

    email = models.EmailField(_('email address'), blank=True)
    message = models.TextField(blank=True)

    class Meta:
        verbose_name = _('FeedBack')

    def __str__(self):
        return self.email


class UserOtpVerify(WynventPostgresDBBaseModel):
    """model for otp verification"""

    phone = models.CharField(max_length=50)
    pass_code = models.CharField(max_length = 10,default='0000')
    verified = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('OtpVerification')

    def __str__(self):
        return self.phone