# coding=utf-8

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import logout

from functools import wraps


def check_authorized(view_func):
    """Decorator which ensures request session is authenticated and will raise a HTTP401 if unauthenticated."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs) if request.user.is_authenticated() else JsonResponse({"error":"Authentication credentials were not provided."}, status=401)
    return _wrapped_view


def check_superuser(view_func):
    """
        Decorator which ensures request session is authenticated and is a superuser
    """

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_active and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            logout(request)
            return redirect('admin:login')

    return _wrapped_view
