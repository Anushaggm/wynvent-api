from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from utils.helpers import ErrorType

from applications.blog.models import TalkToExpert
from applications.blog.serializer import TalkToExpertSerializer, ExpertListSerializer, ExpertResponseSerializer
from applications.ourexperts.models import OurExperts


class TalkToExpertsListView(APIView, ErrorType):
    """
    Returns talk to expert details.

    Request Methods : [GET]
    """
    serializer_class = TalkToExpertSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.blog.serializer.TalkToExpertSerializer
        """
        experts = TalkToExpert.objects.all()
        serializer = self.serializer_class(experts, many=True).data
        return Response(serializer)

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.blog.serializer.TalkToExpertSerializer
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)


class ListExperts(APIView, ErrorType):
    """
    Returns all experts
    """
    serializer_class = ExpertResponseSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.blog.serializer.TalkToExpertSerializer
        """
        experts = OurExperts.objects.all()
        serializer = ExpertListSerializer(experts, many=True).data
        return Response(serializer)

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.blog.serializer.TalkToExpertSerializer
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)