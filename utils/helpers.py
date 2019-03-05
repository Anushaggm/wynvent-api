# coding=utf-8

import re
import os
import six
import time, json
import string
import requests, ast
import pytz
from random import Random, randint

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

# from boto.s3.connection import S3Connection, Bucket, Key
import boto3

from rest_framework import status
from utils.constants import FB_GRAPH_API_PROFILE_URL, PROFILE_IMAGE_DIR, PROPERTY_IMAGE_DIR
from twilio.rest import Client

client = boto3.client('s3')

USING_AWS_S3 = getattr(settings, 'USE_AWS_S3', False)


class ErrorType(object):

    NOT_AUTHORIZED = status.HTTP_401_UNAUTHORIZED
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    SUCCESS = status.HTTP_200_OK
    MISSING_ATTRIBUTES = status.HTTP_206_PARTIAL_CONTENT
    NOT_MODIFIED = status.HTTP_304_NOT_MODIFIED
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    CONFLICT = status.HTTP_409_CONFLICT
    NOT_ACCEPTABLE = status.HTTP_406_NOT_ACCEPTABLE
    NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED
    NO_CONTENT = status.HTTP_204_NO_CONTENT


class ValidateFBAccessToken(object):

    def __init__(self, access_token, data):
        self.access_token = access_token
        self.data_to_validate = data

    def is_valid(self):
        result = False
        url = FB_GRAPH_API_PROFILE_URL + '?access_token=' + self.access_token
        r = requests.get(url)
        response = r.json()
        for key in self.data_to_validate.keys():
            result = True if self.data_to_validate[key] == response.get(key, None) else False
        return result


def send_user_register_email(user):
    """
    Send registration email to user.
    :param user:
    :return:
    """
    from django.contrib.sites.models import Site
    to_email = user.email
    subject = "Welcome to Wynvent"
    ctx = {
        'user': user,
        'site': Site.objects.get(pk=1)
    }
    t = get_template('registration/user_register_email.html')
    c = ctx
    message = t.render(c)
    msg = EmailMessage(subject, message, to=[to_email], from_email=settings.DEFAULT_FROM_EMAIL)
    msg.content_subtype = 'html'
    msg.send()


IDENTIFIER_REGEX = re.compile('^[\w\d_]+\.[\w\d_]+\.\d+$')


def haystack_custom_get_identifier(obj_or_string):
    """
    Get an unique identifier for the object or a string representing the
    object.

    If not overridden, uses <app_label>.<object_name>.<pk>.
    """
    if isinstance(obj_or_string, six.string_types):
        if not IDENTIFIER_REGEX.match(obj_or_string):
            raise AttributeError(u"Provided string '%s' is not a valid identifier." % obj_or_string)

        return obj_or_string

    return u"%s" % (obj_or_string._get_pk_val())


def get_new_static_resource_path(instance, filename, folder_name=''):
    return os.path.join(folder_name, filename)


def get_new_avatar_path(instance, filename):
    return get_new_static_resource_path(instance, filename, PROFILE_IMAGE_DIR)


def get_new_property_image_path(instance, filename):
    file_length = len(filename)
    if file_length > 70:  # If file name is longer than 70, truncate filename
        offset = file_length - (file_length % 40 + 20)  # modulus of file name + 20 to prevent file type truncation
        filename = filename[offset:]
    return get_new_static_resource_path(instance, filename, PROPERTY_IMAGE_DIR)


def direct_s3_upload(imgfile, user):
    timestamp = str(timezone.now()).replace('.', '').replace(' ', '').replace(':', '').replace('+', '')
    img_type = "%s%s" % (user.id, timestamp)
    extension = imgfile.name.split(".")[-1].lower()
    if user.profile_image:
        existing_img = user.profile_image
        ext = existing_img.name.split('.')
        if ext:
            existing_ext = ext[-1].lower()
            try:
                ext_img_type = ext[-2].split('/')[-1].replace('user_', '')
                remove_from_amazon_s3('user', existing_ext, PROFILE_IMAGE_DIR, type=ext_img_type)
            except Exception as e:
                print(e)
    img_name = '%s_%s.%s' % ('user', img_type, extension)
    user.profile_image.save(img_name, ContentFile(imgfile.read()))
    return user.profile_image.url
    # path = default_storage.save(img_name, ContentFile(imgfile.read()))
    # img_url = '%s%s' % (settings.MEDIA_URL, path)
    # print(img_url, "V#######")
    # user.profile_image = img_url
    # user.save()
    # print(user.profile_image, "22222222#######")
    # return img_url


def remove_from_amazon_s3(slug, extension, dir, type=None):

    def get_path(type, extension):
        path = '%s/%s/%s_%s.%s' % (settings.MEDIA_URL.strip("/"), dir, slug, type, extension)
        return path

    def remove_from_bucket(path):
        client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=path)

    if type:
        path = get_path(type, extension)
        remove_from_bucket(path)
    else:
        for type in ['sq1x', 'sq2x', 'sq3x', 'wide1x', 'wide2x', 'wide3x']:
            path = get_path(type, extension)
            remove_from_bucket(path)


def save_media_to_dir(files, name_key, dir, key_to_preserve_old=None):

    """
    Saves files to specified dir in MEDIA root.
    :param files:
    :param dir:
    :param name_key:
    :param key_to_preserve_old:
    :return:
    """
    img_ref = None
    for key in files.keys():
        img = files.get(key)
        if img:
            extension = img.name.split(".")[-1].lower()
            img_ref = '%s%s/%s.%s' % (settings.MEDIA_URL, dir, name_key, extension)
            if USING_AWS_S3:
                img_ref = img_ref.replace(settings.MEDIA_URL, '')

            name_string = "%s%s" % (name_key, key_to_preserve_old) if key_to_preserve_old else name_key
            img_name = '%s/%s_%s.%s' % (dir, name_string, key, extension)
            remove_media_if_exists(name_string, extension, dir, type=key)
            path = default_storage.save(img_name, ContentFile(img.read()))
    return img_ref


def remove_media_if_exists(slug, extension, dir, type=None):

    """
    Removes a file with given path in MEDIA_ROOT
    """

    if USING_AWS_S3:
        return remove_from_amazon_s3(slug, extension, dir, type)

    def remove_from_path(path):

        try:
            os.remove(path)
        except OSError:
            pass

    def get_path(type, extension):
        return os.path.join(settings.MEDIA_ROOT, dir) + '/%s_%s.%s' % (slug, type, extension)

    if type is None:
        for type in ['sq1x', 'sq2x', 'sq3x', 'wide1x', 'wide2x', 'wide3x']:
            path = get_path(type, extension)
            remove_from_path(path)
    else:
        path = get_path(type, extension)
        remove_from_path(path)


def property_complete_percentage(prop):
    """
    Return property complete percentage
    :param prop: Property object
    :return:
    The progress bar will only reach 100% if all fields are completed.
    """
    pending = []

    def _get_count_message(value, message, count):
        if value:
            count += 1
        else:
            pending.append(str(message))
        return count

    count = 0
    if prop.type in ["residential_apartment","residential_villa"]:
        total_count = 32
    if prop.type in ["commercial_showroom"]:
        total_count = 38
    if prop.type in ["commercial_shop"]:
        total_count = 36
    # total_count = 60
    count = _get_count_message(prop.name, _('Name'), count)
    count = _get_count_message(prop.property_for, _('Property For'), count)
    count = _get_count_message(prop.type, _('Type'), count)
    count = _get_count_message(prop.address, _('Address'), count)
    count = _get_count_message(prop.locality, _('Locality'), count)
    count = _get_count_message(prop.city, _('City'), count)
    count = _get_count_message(prop.zipcode, _('Zipcode'), count)
    count = _get_count_message(prop.video_link, _('Video link'), count)
    count = _get_count_message(prop.facilities.all().count() > 0, _('Facilities'), count)
    # count = _get_count_message(prop.building_name, _('Building Name'), count)
    if prop.type in ["residential_apartment","residential_villa"]:
        count = _get_count_message(prop.bedroom_count, _('Bedroom Count'), count)
        count = _get_count_message(prop.bathroom_count, _('Bathroom Count'), count)
        count = _get_count_message(prop.balcony_count, _('Balcony Count'), count)
        count = _get_count_message(prop.age_of_construction, _('Age of construction'), count)
        count = _get_count_message(prop.rent_to_bachelors, _('Rent to bachelors'), count)
        count = _get_count_message(prop.rent_to_family, _('Rent to family'), count)
        count = _get_count_message(prop.rent_to_non_vegetarians, _('Rent to non vegetarians'), count)
        count = _get_count_message(prop.rent_to_with_pets, _('Rent to with pets'), count)
    # count = _get_count_message(prop.puja_room, _('Pooja Room'), count)
    # count = _get_count_message(prop.study_room, _('Study Room'), count)
    # count = _get_count_message(prop.store_room, _('Store Room'), count)
    count = _get_count_message(prop.parking_count_two, _('Parking Count Two wheeler'), count)
    count = _get_count_message(prop.parking_count_four, _('Parking Count Four wheeler'), count)
    count = _get_count_message(prop.furnished_status, _('Furnished'), count)
    if prop.type in ["commercial_showroom","commercial_shop"]:
        count = _get_count_message(prop.washrooms, _('Washroom'), count)
        count = _get_count_message(prop.main_road_facing, _('Road Facing'), count)
    # count = _get_count_message(prop.personal_washroom, _('Personal washroom'), count)
        count = _get_count_message(prop.corner_shop, _('Corner shop'), count)
        count = _get_count_message(prop.pantry, _('Pantry'), count)
        count = _get_count_message(prop.is_corner_plot, _('Corner'), count)
        count = _get_count_message(prop.plot_area, _('Plot Area'), count)
        count = _get_count_message(prop.plot_area_unit, _('Plot Area unit'), count)
        count = _get_count_message(prop.plot_length, _('Plot length'), count)
        count = _get_count_message(prop.plot_length_unit, _('Plot length unit'), count)
        count = _get_count_message(prop.plot_width, _('Plot width'), count)
        count = _get_count_message(prop.plot_width_unit, _('Plot width unit'), count)
        count = _get_count_message(prop.carpet_area, _('Carpet area'), count)
        count = _get_count_message(prop.carpet_area_unit, _('Carpet area unit'), count)
        count = _get_count_message(prop.transaction_type, _('Transaction type'), count)
        count = _get_count_message(prop.price_per_sq_yard, _('price per sq yard'), count)
    if prop.type in ["residential_apartment","residential_villa","commercial_showroom"]:
        count = _get_count_message(prop.total_floor_count, _('Floor'), count)
        count = _get_count_message(prop.floor_number, _('Floor number'), count)
    if prop.type == "residential_villa":
        count = _get_count_message(prop.width_of_road_facing_plot, _('Width of road facing'), count)
        count = _get_count_message(prop.no_of_open_sides, _('Open sides'), count)
    count = _get_count_message(prop.covered_area, _('Covered Area'), count)
    count = _get_count_message(prop.covered_area_unit, _('Covered Area unit'), count)
    count = _get_count_message(prop.available_from_date, _('From date'), count)
    count = _get_count_message(prop.available_immediately, _('Available'), count)

    if prop.type == "residential_apartment":
        count = _get_count_message(prop.owners_residence, _('Owner residence'), count)
    if prop.property_for == "rent" and prop.type in ["residential_apartment","residential_villa"]:
        count = _get_count_message(prop.monthly_rent, _('Monthly rent'), count)
        count = _get_count_message(prop.maintenance_charges, _('Maintenance  charges'), count)
        count = _get_count_message(prop.water_charges, _('Water  charges'), count)
        count = _get_count_message(prop.electricity_charges, _('Electricity  charges'), count)
        count = _get_count_message(prop.security_deposit, _('Security deposit'), count)
    if not prop.property_for == "rent" and prop.type in ["residential_apartment","residential_villa"]:
        count = _get_count_message(prop.other_charges, _('Other  charges'), count)
        count = _get_count_message(prop.expected_price, _('Expected price'), count)
    if not prop.property_for == "rent" and prop.type in ["commercial_showroom","commercial_shop"]:
        count = _get_count_message(prop.other_charges, _('Other  charges'), count)
        count = _get_count_message(prop.expected_price, _('Expected price'), count)
    # count = _get_count_message(prop.total_price, _('Total price'), count)

    count = _get_count_message(prop.exclude_duty_and_reg_charges, _('exclude duty charges'), count)
    count = _get_count_message(prop.interesting_details, _('Interesting details'), count)
    count = _get_count_message(prop.landmarks_and_neighbourhood, _('Landmark'), count)
    # count = _get_count_message(prop.terms_agreed, _('Terms'), count)
    percentage = (count*100) / total_count if count else 0
    print(count,'=============================',percentage)
    pending_text = ', '.join(pending) if pending else '0%'
    return {'pending_text': _('Pending: ') + pending_text, 'percentage': int(percentage)}

def send_user_property_activities(user,message):
    """
    Send email to user regarding submit property and delete property.
    """
    to_email = user.email
    subject = "Welcome to Wynvent"
    msg = EmailMessage(subject, message, to=[to_email], from_email=settings.DEFAULT_FROM_EMAIL)
    msg.send()

def alert_by_sms(phone_no, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
                    to=phone_no,
                    from_=settings.FROM_PHONE,
                    body=message,
                )


def as_utc(dt):
    """
    Return a UTC formatted datetime value
    :param dt:
    :return:
    """
    utc = pytz.timezone("UTC")
    return utc.localize(dt, is_dst=True)