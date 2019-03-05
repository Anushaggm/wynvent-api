# coding=utf-8

from rest_framework import permissions

from .helpers import ErrorType
from .permissions import WynventCurdPermission


class UserRequired(ErrorType):
    """
    Mixin to check if the user is authenticated.

    If user is not authenticated HTTP 401 UNAUTHORISED will raise.
    """

    permission_classes = (permissions.IsAuthenticated, )


class AccessPermission(ErrorType):
    permission_classes = ()
    # permission_classes = (permissions.IsAuthenticated, WynventCurdPermission)



