import requests
from urllib.parse import urlsplit

from django.conf import settings
from django.utils import timezone
from django.core.files import File
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.core.files.temp import NamedTemporaryFile

from applications.marketingproperty.models import Propertydetails, Images
from applications.property.models import Property, PropertyImage
from applications.accounts.models import User
from applications.locations.models import City,Locality
from utils.constants import FB_GRAPH_API_PROFILE_URL, PROPERTY_IMAGE_DIR, MARKETING_PROPERTY_TYPE_LIST, \
    MARKETING_PROPERTY_SUBTYPE_LIST, MARKETING_PROPERTY_SUBTYPE_MAPPINGS


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Import property entries from external DB.
        """
        admin = User.objects.filter(is_superuser=True).latest('email')
        user = User.objects.get(email=admin.email)
        sorted_properties = Propertydetails.objects.filter(property_subtype__in=MARKETING_PROPERTY_SUBTYPE_LIST,
                                                           city__in=settings.IMPORT_CITY).using('properties')
        for property in sorted_properties:
            try:
                try:
                    new_property = Property.objects.get(marketing_property_id=property.property_id)
                    for image in new_property.get_images.all():
                        image.delete()
                except:
                    new_property = Property()
                    new_property.marketing_property_id = property.property_id
                if property.project_name:
                    new_property.name = property.project_name.strip()
                else:
                    new_property.name = property.property_subtype+' in '+property.city
                new_property.user = user
                new_property.address = property.full_address
                new_property.property_for = 'sale'
                new_property.city = property.city
                new_property.locality = property.locality
                if property.bedroom:
                    bedroom_count =  property.bedroom
                    new_property.bedroom_count = bedroom_count
                if property.bathroom:
                    bathroom_count = property.bathroom
                    new_property.bathroom_count = bathroom_count
                if property.car_park:
                    car_park = property.car_park
                    new_property.parking_count_four = car_park
                if property.no_of_open_sides:
                    new_property.no_of_open_sides = property.no_of_open_sides
                if property.length:
                    new_property.plot_length = property.length
                new_property.total_floor_count = property.property_total_floors
                new_property.transaction_type = property.transaction_type
                new_property.other_charges = property.other_charges

                #Mapping property type

                type_temp = "%s_%s" % (property.property_type.lower(), property.property_subtype.lower())
                if type_temp in MARKETING_PROPERTY_TYPE_LIST:
                    new_property.type = type_temp

                new_type = map_subtype(property.property_subtype.lower())
                if not new_type:
                    continue
                new_property.type = new_type

                if "Address:" in property.full_address:
                    full_address = property.full_address.replace("Address:", "")
                    address = full_address
                else:
                    address = property.full_address
                api_key = "AIzaSyDusXtg0H22L3llpSWtZdayiefY52eqs7M"
                api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
                api_response_dict = api_response.json()

                if api_response_dict['status'] == 'OK':

                    latitude = api_response_dict['results'][0]['geometry']['location']['lat']
                    longitude = api_response_dict['results'][0]['geometry']['location']['lng']
                    ref_location = Point(longitude, latitude)
                    new_property.coordinates = ref_location
                else:
                    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(property.locality, api_key))
                    api_response_dict = api_response.json()
                    if api_response_dict['status'] == 'OK':
                        latitude = api_response_dict['results'][0]['geometry']['location']['lat']
                        longitude = api_response_dict['results'][0]['geometry']['location']['lng']
                        ref_location = Point(longitude, latitude)
                        new_property.coordinates = ref_location
                if property.city and property.locality:
                    try:
                        get, created = City.objects.get_or_create(name=property.city.title())
                        get.coordinates = new_property.coordinates
                        get.save()
                        get_locality, create = Locality.objects.get_or_create(city=get, name=property.locality.title())
                        get_locality.coordinates = new_property.coordinates
                        get_locality.save()
                    except Exception as e:
                        continue
                new_property.save()
                marketing_images = Images.objects.filter(property_id=property.property_id).using('properties')
                for img in marketing_images:
                    r = requests.get(img.image_url)
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(r.content)
                    img_temp.flush()
                    img_filename = urlsplit(img.image_url).path[1:]
                    timestamp = str(timezone.now()).replace('.', '').replace(' ', '').replace(':', '').replace('+', '')
                    img_type = "%s%s" % (user.id, timestamp)
                    extension = img.image_url.rsplit('/', 1)[1].split(".")[-1].lower()
                    img_filename = '%s_%s.%s' % ('property', img_type, extension)
                    propery_image = PropertyImage.objects.create(property=new_property)
                    propery_image.image.save(img_filename, File(img_temp))
            except Exception as e:
                continue

def map_subtype(value):
    for key in MARKETING_PROPERTY_SUBTYPE_MAPPINGS:
        if key[0] == value:
            return key[1]
    return None