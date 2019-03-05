from rest_framework import serializers, fields

from applications.builder.models import Builder
from applications.locations.models import City
from applications.locations.serializer import CitySerializer
from applications.property.models import Property, PropertyType
from applications.property.serializers import PropertyListSerializer
from applications.agent.serializer import PropertyTypeSerializer
from utils.constants import *


class BuilderDetailSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving builder details.
    """
    property = serializers.SerializerMethodField()

    def get_property(self, obj):
        return  PropertyListSerializer(obj.user_builder.get_properties.all(), many=True).data

    class Meta:
        model = Builder
        fields = "__all__"


class BuilderRegisterSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving builder details.
    """
    property_type = PropertyTypeSerializer(many=True, read_only=True)
    property_type_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PropertyType.objects.all(), write_only=True
    )
    property_type_list = serializers.ListField(required=False)

    def create(self, validated_data):
        property_types = validated_data.pop('property_type_ids', [])
        property_types = validated_data.pop('property_type_list', [])
        builder = Builder.objects.create(**validated_data)
        property_types = property_types[0].split(",")
        selected_property_types = [int(i) for i in property_types]
        for type in PropertyType.objects.all():
            if type.id in selected_property_types:
                builder.property_type.add(type)
        return builder

    def update(self, instance, validated_data):
        property_type_ids = validated_data.pop('property_type_ids', [])
        property_types = validated_data.pop('property_type_list', [])
        property_types = property_types[0].split(",")
        selected_property_types = [int(i) for i in property_types]
        for type in PropertyType.objects.all():
            if type.id not in selected_property_types:
                instance.property_type.remove(type)
        # Add property type instances that are in the request
        for type in selected_property_types:
            instance.property_type.add(type)

    class Meta:
        model = Builder
        fields = "__all__"