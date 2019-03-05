from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from utils.helpers import ErrorType

from applications.accounts.models import FeedBack
from applications.accounts.serializer import FeedbackSerializer


class FeedbackListView(APIView, ErrorType):
    """
    Returns feedback details.

    Request Methods : [GET]
    """
    serializer_class = FeedbackSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.feedback.serializer.FeedbackSerializer
        """
        feedback = FeedBack.objects.all()
        serializer = self.serializer_class(feedback, many=True).data
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

