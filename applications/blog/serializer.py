from rest_framework import serializers

from applications.blog.models import Blog, BlogAuthor, BlogType, BlogImage, TalkToExpert
from applications.ourexperts.models import OurExperts, ExpertResponses
from zinnia.models.entry import Entry
from zinnia.models.category import Category
from zinnia.models_bases.entry import CoreEntry, CategoriesEntry


class BlogAuthorSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving blog author details.
    """
    class Meta:
        model = BlogAuthor
        fields = "__all__"


class BlogTypeSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving blog type details.
    """

    class Meta:
        model = BlogType
        fields = ['name']


class BlogDetailSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving blog details.
    """
    author = BlogAuthorSerializer()
    type = BlogTypeSerializer()

    class Meta:
        model = Blog
        fields = "__all__"


class BlogImageSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving blog image details.
    """

    class Meta:
        model = BlogImage
        fields = "__all__"


class TalkToExpertSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving blog image details.
    """

    class Meta:
        model = TalkToExpert
        fields = "__all__"


class ExpertListSerializer(serializers.ModelSerializer):
    """serializer for retrieving expert details
    """

    class Meta:
        model = OurExperts
        fields = "__all__"


class ExpertResponseSerializer(serializers.ModelSerializer):
    """serializer for saving expert responses
    """

    class Meta:
        model = ExpertResponses
        fields = "__all__"


class CoreEntrySerializer(serializers.Serializer):

    class Meta:
        model = CoreEntry
        fields = "__all__"


class BlogCategorySerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving blog category details.
    """

    class Meta:
        model = Category
        exclude = ("parent",)


class ZinniaListSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    def get_author(self,obj):
        return BlogAuthorSerializer(obj.authors).data

    def get_categories(self,obj):
        return BlogCategorySerializer(obj.categories).data

    class Meta:
        model = Entry
        fields = "__all__"
