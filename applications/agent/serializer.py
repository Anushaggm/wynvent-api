from rest_framework import serializers

from applications.agent.models import Agent, AgentResponse
from applications.property.models import PropertyType
from applications.property.serializers import PropertyListSerializer


class PropertyTypeSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving facilities.
    """

    class Meta:
        model = PropertyType
        fields = "__all__"


class AgentDetailSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving agent details.
    """
    property = serializers.SerializerMethodField()

    def get_property(self, obj):
        return  PropertyListSerializer(obj.user_agent.get_properties.all(), many=True).data

    class Meta:
        model = Agent
        fields = "__all__"


class AgentRegisterSerializer(serializers.ModelSerializer):
    """
    serializer for agent registration
    """
    property_type = PropertyTypeSerializer(many=True, read_only=True)
    property_type_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PropertyType.objects.all(), write_only=True
    )
    property_type_list = serializers.ListField(required=False)

    def create(self, validated_data):
        property_types = validated_data.pop('property_type_ids', [])
        property_types = validated_data.pop('property_type_list', [])
        agent = Agent.objects.create(**validated_data)
        property_types = property_types[0].split(",")
        selected_property_types = [int(i) for i in property_types]
        for type in PropertyType.objects.all():
            if type.id in selected_property_types:
                agent.property_type.add(type)
        return agent

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
        model = Agent
        fields = "__all__"


class AgentResponseSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving and creating Agent responses.
    """

    class Meta:
        model = AgentResponse
        fields = "__all__"
