from collections import OrderedDict

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from utils.helpers import ErrorType

from applications.blog.models import Blog, BlogAuthor, BlogType, BlogImage
from applications.blog.serializer import BlogDetailSerializer, ZinniaListSerializer, CoreEntrySerializer, BlogCategorySerializer
from zinnia.models.entry import Entry
from zinnia.models.category import Category
from zinnia.models_bases.entry import CoreEntry


class BlogListView(APIView, ErrorType, PageNumberPagination):
    """
    Returns blog details.

    Request Methods : [GET]
    """
    serializer_class = BlogDetailSerializer
    page_size = 10
    max_page_size = 1000

    def get(self, request, format=None):

        """
        Request Methods : [GET]
        ---
        serializer: applications.blog.serializer.BlogDetailSerializer
        """
        page = self.request.GET.get('page', 1)
        blogs = Blog.objects.all()

        # Get blogs under a type
        blog_type_id = self.request.GET.get('type__id')
        if blog_type_id:
            blog_type = get_object_or_404(Blog, id=blog_type_id)
            blogs = blogs.filter(type=blog_type)

        # Order by popularity
        if self.request.GET.get('sort_popularity'):
            blogs = blogs.order_by("get_views")

        # Order by Most recent
        if self.request.GET.get('most_recent'):
            blogs = blogs.order_by("created")

        data = self.serializer_class(blogs, many=True).data
        paginated_data = self.paginate_queryset(data, request)
        response_data = self.get_paginated_response(paginated_data, page)
        return Response(response_data)

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


class BlogDetailView(APIView, ErrorType):
    """
    Returns blog details.

    Request Methods : [GET]
    """
    serializer_class = BlogDetailSerializer

    def get(self, request, pk, format=None):
        blog = self.get_object(pk)
        serializer = self.serializer_class(blog)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        """
        Request Methods : [DELETE]
        ---
        serializer: applications.blog.serializer.BlogDetailSerializer
        """
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=self.NO_CONTENT)

    def get_object(self, pk):
        """
        To get a specific blog object
        """
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404


class ZinniaListView(APIView, ErrorType):
    serializer_class = ZinniaListSerializer

    def get(self, request, format=None):
        blogs = Entry.objects.all().order_by("-creation_date")[:6]
        serializer = self.serializer_class(blogs, many=True)
        return Response(serializer.data)


class ZinniaDetailView(APIView, ErrorType):
    """
    Returns blog details.

    Request Methods : [GET]
    """
    serializer_class = ZinniaListSerializer

    def get(self, request, id, format=None):
        blog = self.get_object(id)
        serializer = self.serializer_class(blog)
        return Response(serializer.data)

    def get_object(self, pk):
        """
        To get a specific blog object
        """
        try:
            return Entry.objects.get(id=pk)
        except Entry.DoesNotExist:
            raise Http404


class ZinniaCategorys(APIView, ErrorType):
    """
    Returns category lists.

    Request Methods : [GET]
    """
    serializer_class = BlogCategorySerializer

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data)


class BlogList(APIView, ErrorType, PageNumberPagination):
    """
    Returns blogs under specific category.

    Request Methods : [GET]
    """
    serializer_class = ZinniaListSerializer
    page_size = 6
    max_page_size = 1000

    def get(self, request,id, format=None):
        page = self.request.GET.get('page', 1)
        entries = Entry.objects.filter(categories__id=id)

        if self.request.GET.get('most_recent'):
            entries = entries.order_by("-creation_date")

        paginated_data = self.paginate_queryset(entries, request)
        data = self.serializer_class(paginated_data, many=True).data
        response_data = self.get_paginated_response(data, page)
        return Response(response_data)

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