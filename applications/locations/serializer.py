from rest_framework import serializers

from applications.locations.models import City, Locality


class LocalitySerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving locality details.
    """

    class Meta:
        model = Locality
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving city details.
    """

    class Meta:
        model = City
        fields = "__all__"
