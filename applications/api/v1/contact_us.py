from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from utils.helpers import ErrorType

from applications.accounts.models import ContactUs
from applications.accounts.serializer import ContactSerializer, FeedbackSerializer


class ContactListView(APIView, ErrorType):
    """
    Returns contact details.

    Request Methods : [GET]
    """
    serializer_class = ContactSerializer

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.accounts.serializer.ContactDetailSerializer
        """
        contact = ContactUs.objects.all()
        serializer = self.serializer_class(contact, many=True).data
        return Response(serializer)

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.accounts.serializer.ContactDetailSerializer
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=self.SUCCESS)
        return Response(serializer.errors, status=self.BAD_REQUEST)

