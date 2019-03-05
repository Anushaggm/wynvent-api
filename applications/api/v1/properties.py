import random
from random import shuffle
from collections import OrderedDict

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.conf import settings
from django.contrib.gis.geos import Point, GEOSGeometry

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from haystack.query import SearchQuerySet, EmptySearchQuerySet
from haystack.inputs import AutoQuery, Exact, Clean
from applications.general.models import SortConfiguration

from applications.property.models import Property, PropertyResponse, FacilityType
from applications.locations.models import Locality, City
from applications.property.serializers import (
    PropertyListSerializer,
    PropertyModelSerializer,
    PropertySearchSerializer,
    MyPropertyListingSerializer,
    PropertyResponseSerializer,
    FacilityTypeSerializer,
    ShortlistedPropertyActionSerializer,
    PropertyReportSerializer,
    AdvertisementSerializer,
    BannerListSerializer,
    ActivityBasedSerializer,
    UserTimerSerializer,
)
from applications.advertisement.models import Advertisement, Banner, ActivityBasedPopup, UserTimerPopup

from utils.mixins import AccessPermission
from utils.helpers import ErrorType, send_user_property_activities, alert_by_sms
from utils.constants import *


class PropertyListView(AccessPermission, APIView, PageNumberPagination):
    """
    Property Listing API

    Request Methods : [GET]
    """
    serializer_class = PropertyListSerializer
    page_size = 10
    max_page_size = 1000

    def get(self, request, format=None):
        page = self.request.GET.get('page', 1)
        properties = Property.objects.all()

        property_type = self.request.GET.get('type')
        if property_type == "residential":
            properties = properties.filter(type__in=[
                RESIDENTIAL_APARTMENT_PROPERTY_TYPE,
                RESIDENTIAL_VILLA_PROPERTY_TYPE
            ])
        elif property_type == "commercial":
            properties = properties.filter(type__in=[
                COMMERCIAL_SHOWROOM_PROPERTY_TYPE,
                COMMERCIAL_SHOP_PROPERTY_TYPE
            ])

        city = self.request.GET.get('city')
        if city:
            max_dist = D(m=PROPERTY_SEARCH_DISTANCE)
            try:
                get_city = City.objects.get(id=city, coordinates__isnull=False)
                properties = properties.filter(coordinates__distance_lte=(get_city.coordinates, max_dist)).annotate(distance=Distance('coordinates', get_city.coordinates)).order_by('distance')
            except City.DoesNotExist:
                raise Http404

        plot_area_unit = self.request.GET.get('plot_area_unit')
        if plot_area_unit:
            properties = properties.filter(plot_area_unit=plot_area_unit)

        # Order by popularity
        if self.request.GET.get('sort_popularity'):
            properties = properties.order_by("get_views")
        #new in your city
        if self.request.GET.get('latest'):
            properties = properties.order_by("-created")
            # print(properties,'=======================')

        paginated_data = self.paginate_queryset(properties, request)
        data = self.serializer_class(paginated_data, many=True).data
        response_data = self.get_paginated_response(data, page)

        return Response(response_data)

    def get_paginated_response(self, data, page):
        """
        Return a paginated style `Response` object for the given output data.
        """
        return OrderedDict([
            ('count', self.page.paginator.count),
            ('current', page),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])


class PropertyDetailView(AccessPermission, APIView):
    """
    Property Basic API

    Request Methods : [GET, POST, PUT, DELETE]
    """
    serializer_class = PropertyModelSerializer

    def get(self, request, pk, format=None):
        prop = self.get_object(pk)
        serializer = self.serializer_class(prop, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        prop = self.get_object(pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.update(prop, serializer.validated_data)
            return Response(status=self.SUCCESS)
        return Response(serializer.errors, status=self.NOT_AUTHORIZED)

    def delete(self, request, pk, format=None):
        prop = self.get_object(pk)
        message = 'Your property '+prop.name+' has been deleted successfully'
        alert_by_sms(prop.user.mobile, message)
        send_user_property_activities(prop.user, message)
        prop.delete()
        return Response(status=self.SUCCESS)

    def get_object(self, pk):
        """
        To get a specific agent object
        """
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404


class SubmitPropertyView(AccessPermission, APIView, PageNumberPagination):
    """
    Submit a Property

    Request Methods : [POST]
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = PropertyModelSerializer

    def post(self, request, format=None):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.validated_data['id'], status=self.SUCCESS)
        else:
            return Response(serializer.errors, status=self.NOT_AUTHORIZED)


class PropertySearchView(APIView, ErrorType, PageNumberPagination):
    """
    Search for properties based on different filters.

    Request Methods : [GET]
    """
    property_serializer_class = PropertySearchSerializer
    page_size = 10
    max_page_size = 1000

    def get(self, request, *args, **kwargs):
        """
        example:
            /api/v1/property/search/?q=TWO%20BHK%20%APARTMENT
        """
        query = request.GET.get('q')
        min_budget = request.GET.get('min_budget')
        max_budget = request.GET.get('max_budget')
        bedroom_count = request.GET.get('bedroom_count')
        bathroom_count = request.GET.get('bathroom_count')
        puja_room = request.GET.get('puja_room')
        study_room = request.GET.get('study_room')
        store_room = request.GET.get('store_room')
        property_for = request.GET.get('property_for')
        prop_type = request.GET.get('type')
        localities = request.GET.get('localities')
        maintenance_charges = request.GET.get('maintenance_charges')
        min_security_deposit = request.GET.get('min_security_deposit')
        max_security_deposit = request.GET.get('max_security_deposit')
        min_plot_area = request.GET.get('min_plot_area')
        max_plot_area = request.GET.get('max_plot_area')
        user_type = request.GET.get('user_type')
        rent_to_bachelors = request.GET.get('rent_to_bachelors')
        rent_to_family = request.GET.get('rent_to_family')
        rent_to_non_vegetarians = request.GET.get('rent_to_non_vegetarians')
        rent_to_with_pets = request.GET.get('rent_to_with_pets')
        facilities = request.GET.getlist('facilities')
        city = request.GET.get('city')
        loc = request.GET.get('loc', '')
        sort = request.GET.get('sort_by')
        list_by = request.GET.getlist('list_by')

        sqs = SearchQuerySet()
        if query:
            sqs = sqs.filter(content=AutoQuery(query))
            # sqs = sqs.autocomplete(name_auto=query)  # Autocomplete using EdgeNgramField
        if min_budget:
            sqs = sqs.filter(expected_price__gte=Clean(min_budget))
        if max_budget:
            sqs = sqs.filter(expected_price__lte=Clean(max_budget))
        if bedroom_count:
            sqs = sqs.filter(bedroom_count=Clean(bedroom_count))
        if bathroom_count:
            sqs = sqs.filter(bathroom_count=Clean(bathroom_count))
        if puja_room:
            sqs = sqs.filter(puja_room=Clean(puja_room))
        if study_room:
            sqs = sqs.filter(study_room=Clean(study_room))
        if store_room:
            sqs = sqs.filter(store_room=Clean(store_room))
        if property_for:
            sqs = sqs.filter(property_for=Clean(property_for))
        if prop_type:
            sqs = sqs.filter(type=Clean(prop_type))
        if maintenance_charges:
            sqs = sqs.filter(maintenance_charges=maintenance_charges)
        if min_security_deposit:
            sqs = sqs.filter(security_deposit__gte=Clean(min_security_deposit))
        if max_security_deposit:
            sqs = sqs.filter(security_deposit__lte=Clean(max_security_deposit))
        if min_plot_area:
            sqs = sqs.filter(plot_area__gte=Clean(min_plot_area))
        if max_plot_area:
            sqs = sqs.filter(plot_area__lte=Clean(max_plot_area))
        if user_type:
            sqs = sqs.filter(user_type=Clean(user_type))
        if rent_to_bachelors:
            sqs = sqs.filter(rent_to_bachelors=Clean(rent_to_bachelors))
        if rent_to_family:
            sqs = sqs.filter(rent_to_family=Clean(rent_to_family))
        if rent_to_non_vegetarians:
            sqs = sqs.filter(rent_to_non_vegetarians=Clean(rent_to_non_vegetarians))
        if rent_to_with_pets:
            sqs = sqs.filter(rent_to_with_pets=Clean(rent_to_with_pets))
        if facilities:
            sqs = sqs.filter(facilities__in=Clean(facilities))
        # if places:
        #     sqs = sqs.filter(locality__in=Clean(places))
        if sort == SORT_BY_PROXIMITY:
            sqs = sqs.order_by('-created')
        if sort == SORT_BY_AGE_OF_CONSTRUCTION:
            sqs = sqs.order_by('-age_of_construction')
        if sort == "view_count":
            sqs = sqs.order_by('-view_count')
        if sort == "click_count":
            sqs = sqs.order_by('-click_count')
        if sort == "contact_count":
            sqs = sqs.order_by('-response_count')

        if not sort in SORT_VAL_LIST:
            sort_conf = SortConfiguration.get_solo()
            if sort_conf.builder_sort == VIEW_COUNT:
                sqs = sqs.order_by('-view_count')
            if sort_conf.builder_sort == CLICK_COUNT:
                sqs = sqs.order_by('-click_count')
            if sort_conf.builder_sort == RESPONSE_COUNT:
                sqs = sqs.order_by('-response_count')
            if sort_conf.builder_sort == PROXIMITY:
                sqs = sqs.order_by('-proximity')


        if list_by:
            sqs = sqs.filter(user_type__in=Clean(list_by))

        lat_lng = loc.split(',')
        if len(lat_lng) == 2:
            lat = lat_lng[0]
            lng = lat_lng[1]
            sqs = self.execute_coordinates_search(lat, lng, sqs, PROPERTY_SEARCH_DISTANCE)
        if city:
            sqs = self.execute_city_search(city, sqs, PROPERTY_SEARCH_DISTANCE)

        if localities:
            sqs = self.execute_locality_search(localities, sqs, 5000)

        page = self.request.GET.get('page', 1)
        paginated_data = self.paginate_queryset(sqs, request)
        data = self.property_serializer_class(paginated_data, many=True).data
        response_data = self.get_paginated_response(data, page)

        return Response(response_data)

    def execute_coordinates_search(self, lat, lng, sqs, distance):
        max_dist = D(m=distance)
        location = Point((float(lng), float(lat)))
        sqs = sqs.dwithin('location', location, max_dist).distance('location', location)
        sorted_sqs = sqs.order_by('distance')
        return sorted_sqs

    def execute_locality_search(self, localities, sqs, distance):
        locality_ids = list(filter(None, localities.split(',')))
        localities = Locality.objects.filter(id__in=locality_ids, coordinates__isnull=False)
        max_dist = D(m=distance)

        # If localities are more than one
        if localities.count() > 1:
            locality_result_ids = []
            original_sqs = sqs
            for locality in localities:
                coordinates = locality.coordinates
                locality_sqs = sqs.dwithin('location', coordinates, max_dist).distance('location', coordinates)
                locality_result_ids.extend(locality_sqs.values_list("id", flat=True))
            locality_result_ids = list(set(locality_result_ids))
            sqs = original_sqs.filter(id__in=locality_result_ids)
            sorted_sqs = sqs
            return sorted_sqs
        else:
            for locality in localities:
                locality = locality
                coordinates = locality.coordinates
                sqs = sqs.dwithin('location', coordinates, max_dist).distance('location', coordinates)
                sorted_sqs = sqs.order_by('distance')
                return sorted_sqs

    def execute_city_search(self, city, sqs, distance):
        try:
            city = City.objects.get(id=city)
            max_dist = D(m=distance)
            coordinates = city.coordinates
            sqs = sqs.dwithin('location', coordinates, max_dist).distance('location', coordinates)
            sorted_sqs = sqs.order_by('distance')
            return sorted_sqs
        except City.DoesNotExist:
            raise Http404

    def get_paginated_response(self, data, page):
        """
        Return a paginated style `Response` object for the given output data.
        """
        return OrderedDict([
            ('count', self.page.paginator.count),
            ('current', page),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])


class MyPropertyListingsView(AccessPermission, APIView, PageNumberPagination):
    """
    Property Listings by a user

    Request Methods : [GET, POST, PUT, DELETE]
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = MyPropertyListingSerializer
    page_size = 3
    max_page_size = 1000

    def get(self, request, format=None):
        page = self.request.GET.get('page', 1)
        properties = Property.objects.filter(user=request.user).order_by("-created")
        data = self.serializer_class(properties, many=True).data

        paginated_data = self.paginate_queryset(data, request)
        response_data = self.get_paginated_response(paginated_data, page)
        return Response(response_data)

    def get_paginated_response(self, data, page):
        """
        Return a paginated style `Response` object for the given output data.
        """
        return OrderedDict([
            ('count', self.page.paginator.count),
            ('current', page),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])


class PropertyResponsesView(APIView, ErrorType):
    """
    Returns property responses.

    Request Methods : [GET, POST]
    """
    # permission_classes = (permissions.IsAuthenticated, )
    serializer_class = PropertyResponseSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.property.serializers.PropertyResponseSerializer
        """
        property_responses = PropertyResponse.objects.filter(owner=request.user).order_by("-timestamp")
        property_id = request.GET.get('property_id')
        if property_id:
            property_responses = property_responses.filter(property__id=property_id)
        serializer = self.serializer_class(property_responses, many=True).data
        return Response(serializer)

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.property.serializers.PropertyResponseSerializer
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)


class ShortlistedPropertiesView(AccessPermission, APIView, PageNumberPagination):
    """
    Shortlisted properties by a user

    Request Methods : [GET, POST, PUT, DELETE]
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = PropertyListSerializer
    page_size = 3
    max_page_size = 1000

    def get(self, request, format=None):
        page = self.request.GET.get('page', 1)
        properties = request.user.shortlisted_properties.all()
        data = self.serializer_class(properties, many=True).data

        paginated_data = self.paginate_queryset(data, request)
        response_data = self.get_paginated_response(paginated_data, page)
        return Response(response_data)

    def get_paginated_response(self, data, page):
        """
        Return a paginated style `Response` object for the given output data.
        """
        return OrderedDict([
            ('count', self.page.paginator.count),
            ('current', page),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

    def post(self, request, format=None):

        """
        Add or remove a property from user's shortlist.
        Request Methods : [POST]
        ---
        serializer: applications.property.serializers.ShortlistedPropertyActionSerializer
        """
        serializer = ShortlistedPropertyActionSerializer(data=request.data)
        if serializer.is_valid():
            property_id = serializer.validated_data['property_id']
            action = serializer.validated_data['action']
            prop = get_object_or_404(Property, pk=property_id)
            user = request.user
            if action == ADD_TO_SHORTLIST:
                user.shortlisted_properties.add(prop)
            if action == REMOVE_FROM_SHORTLIST:
                if prop in user.shortlisted_properties.all():
                    user.shortlisted_properties.remove(prop)

            return Response(status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)


class FacilityTypeListView(APIView, ErrorType):
    """
    Returns facility types list.

    Request Methods : [GET]
    """
    serializer_class = FacilityTypeSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.property.serializers.FacilityTypeSerializer
        """
        facility_types = FacilityType.objects.all()
        serializer = self.serializer_class(facility_types, many=True).data
        return Response(serializer)


class PropertyReportView(APIView, ErrorType):
    """
    Request Methods : [GET, POST]
    """
    serializer_class = PropertyReportSerializer

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.property.serializers.PropertyResponseSerializer
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)


class AdvertisementListView(APIView, ErrorType):
    """
    Returns advertisements list.

    Request Methods : [GET]
    """
    serializer_class = AdvertisementSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.property.serializers.AdvertisementSerializer
        """
        advertisements = Advertisement.objects.all()
        loc = request.GET.get('location', '')
        try:
            if loc:
                lat_lng = loc.split(',')
                if len(lat_lng) == 2:
                    lat = lat_lng[0]
                    lng = lat_lng[1]
                    advertisements = self.execute_coordinates_search(lat, lng, advertisements, PROPERTY_SEARCH_DISTANCE)
            advertisements = random.sample(list(advertisements), 2)
            advertisement = advertisements
            serializer = self.serializer_class(advertisement, many=True)
            return Response(serializer.data)
        except:
            raise Http404

    def execute_coordinates_search(self, lat, lng, add, distance):
        max_dist = D(m=distance)
        location = Point((float(lng), float(lat)))
        add = add.dwithin('location', location, max_dist).distance('location', location)
        return add


class BannerListView(APIView, ErrorType):
    """
    Returns banners list.

    Request Methods : [GET]
    """
    serializer_class = BannerListSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.property.serializers.BannerListSerializer
        """
        banners = Banner.objects.all()
        property = request.GET.get('property', '')
        normal = request.GET.get('normal', '')
        try:
            if property:
                banners = banners.filter(type="property_banner").order_by('?')[:1]
            if normal:
                banners = banners.filter(type="normal_banner").order_by('?')[:5]
            serializer = self.serializer_class(banners, many=True)
            return Response(serializer.data)
        except:
            serializer = self.serializer_class(banners, many=True)
            return Response(serializer.data)


class ActivityListView(APIView, ErrorType):
    """
    Returns activity based popup data.

    Request Methods : [GET]
    """
    serializer_class = ActivityBasedSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.property.serializers.ActivityBasedSerializer
        """
        popups = ActivityBasedPopup.objects.all()
        new_user = request.GET.get('new_user', '')
        if new_user:
            popups = popups.filter(for_new_user=True)
        popups = popups.order_by('?')[:1]
        serializer = self.serializer_class(popups, many=True)
        return Response(serializer.data)


class UserTimerView(APIView, ErrorType):
    """
    Returns user timer popup data.

    Request Methods : [GET]
    """
    serializer_class = UserTimerSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.property.serializers.UserTimerSerializer
        """
        popups = UserTimerPopup.objects.all()
        new_user = request.GET.get('new_user', '')
        if new_user:
            popups = popups.filter(for_new_user=True)
        popups = popups.order_by('?')[:1]
        serializer = self.serializer_class(popups, many=True)
        return Response(serializer.data)