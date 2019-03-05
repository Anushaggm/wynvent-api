# coding=utf-8

from rest_framework import permissions
from utils.constants import WYNVENT_ADMIN


class WynventCurdPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET' and request.user.is_authenticated():
            return True
        # if request.user.role == WYNVENT_ADMIN:
        #     return True
        return False
