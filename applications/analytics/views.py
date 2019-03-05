# coding=utf-8

from rest_framework.views import APIView
from rest_framework.response import Response


class LogStashDataView(APIView):
    """
    Data view for ELK stack.
    """

    def get(self, request, format=None):
        return Response({})
