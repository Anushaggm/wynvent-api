from collections import OrderedDict

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from utils.helpers import ErrorType

from applications.builder.models import Builder
from applications.accounts.models import User
from applications.builder.serializer import BuilderDetailSerializer, BuilderRegisterSerializer
from applications.general.models import SortConfiguration

from utils.constants import SORT_VAL_LIST, VIEW_COUNT, CLICK_COUNT, PROXIMITY, RESPONSE_COUNT


class BuilderListView(APIView, ErrorType, PageNumberPagination):
    """
    Returns builder details.

    Request Methods : [GET]
    """
    serializer_class = BuilderDetailSerializer
    page_size = 10
    max_page_size = 1000

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.builder.serializer.BuilderDetailSerializer
        """
        page = self.request.GET.get('page', 1)
        builders = Builder.objects.all()
        sort = request.GET.get('sort')
        city = request.GET.get('city')

        if request.GET.get('featured'):
            builders = Builder.objects.filter(featured=True)[:8]
        if sort == "view_count":
            builders = builders.order_by('-view_count')
        if sort == "click_count":
            builders = builders.order_by('-click_count')
        if sort == "contact_count":
            builders = builders.order_by('-response_count')

        if not sort in SORT_VAL_LIST:
            sort_conf = SortConfiguration.get_solo()
            if sort_conf.builder_sort == VIEW_COUNT:
                builders = builders.order_by('-view_count')
            if sort_conf.builder_sort == CLICK_COUNT:
                builders = builders.order_by('-click_count')
            if sort_conf.builder_sort == RESPONSE_COUNT:
                builders = builders.order_by('-response_count')
            if sort_conf.builder_sort == PROXIMITY:
                builders = builders.order_by('-proximity')
        if city:
            builders = builders.filter(city__icontains=city)
        paginated_data = self.paginate_queryset(builders, request)
        data = self.serializer_class(paginated_data, many=True).data
        response_data = self.get_paginated_response(data, page)
        return Response(response_data)

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.builder.serializer.BuilderDetailSerializer
        """
        serializer = BuilderRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)

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


class BuilderDetailView(APIView, ErrorType):
    """
    Returns builder details.

    Request Methods : [GET]
    """
    serializer_class = BuilderDetailSerializer

    def get(self, request, pk, format=None):
        builder = self.get_object(pk)
        serializer = self.serializer_class(builder)
        return Response(serializer.data)

    def post(self, request, pk, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.builder.serializer.BuilderDetailSerializer
        """
        builder = self.get_object(pk)
        serializer = BuilderRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(builder, serializer.validated_data)
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Request Methods : [DELETE]
        ---
        serializer: applications.builder.serializer.BuilderDetailSerializer
        """
        builder = self.get_object(pk)
        builder.delete()
        return Response(status=self.NO_CONTENT)

    def get_object(self, pk):
        """
        To get a specific builder object
        """
        try:
            return Builder.objects.get(pk=pk)
        except Builder.DoesNotExist:

            raise Http404