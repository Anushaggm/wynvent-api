from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from utils.helpers import ErrorType

from applications.locations.models import City, Locality
from applications.locations.serializer import LocalitySerializer, CitySerializer
from utils.constants import *


class LocalityListView(APIView, ErrorType):
    """
    Returns localities list.

    Request Methods : [GET]
    """
    serializer_class = LocalitySerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.feedback.serializer.FeedbackSerializer
        """
        localities = Locality.objects.all()
        id = self.request.GET.get('id')#to get the corresponding localities under city
        if id:
            localities = localities.filter(city__id=id)

        serializer = self.serializer_class(localities, many=True).data
        return Response(serializer)

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.feedback.serializer.FeedbackSerializer
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)


class CityListView(APIView, ErrorType):
    """
    Returns cities list.

    Request Methods : [GET]
    """
    serializer_class = CitySerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.feedback.serializer.FeedbackSerializer
        """
        cities = City.objects.all()
        serializer = self.serializer_class(cities, many=True).data
        return Response(serializer)

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.feedback.serializer.FeedbackSerializer
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)


class LocationPoints(APIView, ErrorType):
    serializer_class = CitySerializer

    def post(self, request, **kwargs):
        key = request.POST.get('city')
        cities = City.objects.get(id=key)
        serializer = self.serializer_class(cities).data
        return Response(serializer)


class NearestCityView(APIView, ErrorType):
    serializer_class = CitySerializer

    def post(self, request, **kwargs):
        location = request.POST.get('location')
        cities = []
        lat_lng = location.split(',')
        if len(lat_lng) == 2:
            lat = lat_lng[0]
            lng = lat_lng[1]
            input_point = Point(float(lat), float(lng), srid=4326)
            cities = City.objects.annotate(distance=Distance('coordinates', input_point)).order_by('distance')[:1]
        serializer = self.serializer_class(cities, many=True).data
        return Response(serializer)


class GetLocalityDetail(APIView, ErrorType):

    serializer_class = LocalitySerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        """
        city = self.request.GET.get('city')
        locality = self.request.GET.get('locality')
        try:
            saved_locality = Locality.objects.get(name=locality, city__id=city)
            serializer = self.serializer_class(saved_locality).data
            return Response(serializer)
        except:
            raise Http404