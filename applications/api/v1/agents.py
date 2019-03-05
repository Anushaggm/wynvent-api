from collections import OrderedDict

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from applications.general.models import SortConfiguration
from utils.constants import SORT_VAL_LIST, VIEW_COUNT, CLICK_COUNT, RESPONSE_COUNT, PROXIMITY

from utils.helpers import ErrorType

from applications.agent.models import Agent, AgentResponse
from applications.agent.serializer import AgentDetailSerializer, AgentResponseSerializer, AgentRegisterSerializer


class AgentListView(APIView, ErrorType, PageNumberPagination):
    """
    Returns agent details.

    Request Methods : [GET, POST]
    """
    serializer_class = AgentDetailSerializer
    page_size = 10
    max_page_size = 1000

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.agent.serializer.AgentDetailSerializer
        """
        page = self.request.GET.get('page', 1)
        agents = Agent.objects.all()
        sort = request.GET.get('sort')
        city = request.GET.get('city')
        if request.GET.get('featured'):
            agents = Agent.objects.filter(featured=True)[:8]
        if sort == "view_count":
            agents = agents.order_by('-view_count')
        if sort == "click_count":
            agents = agents.order_by('-click_count')
        if sort == "contact_count":
            agents = agents.order_by('-response_count')

        if not sort in SORT_VAL_LIST:
            sort_conf = SortConfiguration.get_solo()
            if sort_conf.builder_sort == VIEW_COUNT:
                agents = agents.order_by('-view_count')
            if sort_conf.builder_sort == CLICK_COUNT:
                agents = agents.order_by('-click_count')
            if sort_conf.builder_sort == RESPONSE_COUNT:
                agents = agents.order_by('-response_count')
            if sort_conf.builder_sort == PROXIMITY:
                agents = agents.order_by('-proximity')
        if city:
            agents = agents.filter(city__icontains=city)
        paginated_data = self.paginate_queryset(agents, request)
        data = self.serializer_class(paginated_data, many=True).data
        response_data = self.get_paginated_response(data, page)
        return Response(response_data)

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.agent.serializer.AgentDetailSerializer
        """
        serializer = AgentRegisterSerializer(data=request.data)
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


class AgentDetailView(APIView, ErrorType):
    """
    Returns agent details.

    Request Methods : [GET, POST]
    """
    serializer_class = AgentDetailSerializer

    def get(self, request, pk, format=None):
        agent = self.get_object(pk)
        serializer = self.serializer_class(agent)
        return Response(serializer.data)
    
    def post(self, request, pk, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.agent.serializer.AgentDetailSerializer
        """
        agent = self.get_object(pk)
        serializer = AgentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(agent, serializer.validated_data)
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Request Methods : [DELETE]
        ---
        serializer: applications.agent.serializer.AgentDetailSerializer
        """
        agent = self.get_object(pk)
        agent.delete()
        return Response(status=self.NO_CONTENT)

    def get_object(self, pk):
        """
        To get a specific agent object
        """
        try:
            return Agent.objects.get(pk=pk)
        except Agent.DoesNotExist:
            raise Http404


class AgentResponseListView(APIView, ErrorType):
    """
    Returns agent responses.

    Request Methods : [GET, POST]
    """
    serializer_class = AgentResponseSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.agent.serializer.AgentDetailSerializer
        """
        agent_responses = AgentResponse.objects.all()
        serializer = self.serializer_class(agent_responses, many=True).data
        return Response(serializer)

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.agent.serializer.AgentDetailSerializer
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)
