"""WYNVENT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required

# from applications.api.v1.accounts import PasswordResetLinkView


urlpatterns = [
    url(r'^wynvent-admin/', admin.site.urls),
    url(r'^api/v1/', include('applications.api.v1.urls.internal')),
    url(r'^core/', include('applications.analytics.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^social-accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^api/public/v1/', include('applications.api.v1.urls.public')),
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django_comments.urls')),
]

# static files (images, css, javascript, etc.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
