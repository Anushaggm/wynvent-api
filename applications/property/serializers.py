from django.db.models import Count
from django.contrib.gis.geos import Point

from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField

from applications.property.models import (
    Property,
    PropertyImage,
    PropertyResponse,
    Facility,
    FacilityType,
    PropertyReport,
    PropertyAnalytics
)
from applications.advertisement.models import Advertisement, Banner, ActivityBasedPopup, UserTimerPopup
from utils.helpers import *
from utils.constants import PROPERTY_SHORTLIST_ACTIONS, MONTHS_DICT


class PropertyImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyImage
        fields = "__all__"


class FacilitySerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving facilities.
    """

    class Meta:
        model = Facility
        exclude = (
            "created",
            "modified"
        )


class PropertyListSerializer(serializers.ModelSerializer):
    """ Property model serializer """
    user_type = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            "id",
            "name",
            "property_for",
            "address",
            "locality",
            "city",
            "user_type",
            "created",
            "total_price",
            "thumbnail_url",
            "coordinates",
            "monthly_rent",
            "expected_price",
            "slug",
        )

    def get_user_type(self, obj):
        if obj.user:
            return obj.user.type
        return None

    def get_thumbnail_url(self, obj):
        images = obj.get_images.all()
        if images.exists():
            try:
                return images[0].image.url
            except:
                return None
        return None


class ShortlistedPropertyActionSerializer(serializers.Serializer):
    property_id = serializers.IntegerField(required=True)
    action = serializers.ChoiceField(choices=PROPERTY_SHORTLIST_ACTIONS, required=True)


class PropertyModelSerializer(serializers.ModelSerializer):
    """ Property model serializer """

    coordinates = PointField()
    locality = serializers.CharField(required=True)

    facilities = FacilitySerializer(many=True, read_only=True)
    facility_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Facility.objects.all(), write_only=True
    )
    add_facilities = serializers.ListField(required=False)
    images = PropertyImageSerializer(source="get_images", many=True, read_only=True)
    image_ids = serializers.ListField(
        write_only=True, required=False, child=serializers.FileField(
            max_length=100000, allow_empty_file=False, use_url=False
        )
    )
    old_images = serializers.ListField(required=False, )
    number_of_views = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    shortlisted_status = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = "__all__"

    def create(self, validated_data):
        add_facilities = validated_data.pop('add_facilities', [])
        facility_ids = validated_data.pop('facility_ids', [])
        image_objs = validated_data.pop('image_ids', [])
        old_images = validated_data.pop('old_images', [])
        prop = Property.objects.create(**validated_data)
        if not add_facilities == []:
            add_facilities = add_facilities[0].split(",")
            selected_facilities = [int(i) for i in add_facilities]
            for facility in Facility.objects.all():
                if facility.id in selected_facilities:
                    prop.facilities.add(facility)
        for image in image_objs:
            PropertyImage.objects.create(image=image, property=prop)
        validated_data['id'] = prop.id
        message = 'Your property '+prop.name+' has been created successfully'
        alert_by_sms(prop.user.mobile, message)
        send_user_property_activities(prop.user, message)
        return prop

    def update(self, instance, validated_data):
        # Delete any images not included in the request
        images = validated_data.pop('image_ids', [])
        old_images = validated_data.pop('old_images', [])
        if not old_images == ['']:
            old_images_id = old_images[0].split(",")
            old_images = [int(i) for i in old_images_id]
            for image in instance.get_images.all():
                if not image.id in old_images:
                    image.delete()

        # Remove any facilities not included in the request
        add_facilities = validated_data.pop('add_facilities', [])
        if not add_facilities == []:
            add_facilities = add_facilities[0].split(",")
            for facility in instance.facilities.all():
                if facility.id not in add_facilities:
                    instance.facilities.remove(facility)

        # Create or update image instances that are in the request

        if images:
            for item in images:
                prop_image = PropertyImage(image=item, property=instance)
                prop_image.save()
        # Add facility instances that are in the request
        for facility in add_facilities:
            instance.facilities.add(facility)

        return super(PropertyModelSerializer, self).update(instance, validated_data)

    def get_number_of_views(self, obj):
        return obj.get_views.count()

    def get_user_type(self, obj):
        if obj.user:
            return obj.user.type
        return None

    def get_shortlisted_status(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.is_authenticated():
                return obj in user.shortlisted_properties.all()
        return None


class PropertySearchSerializer(serializers.Serializer):
    """
    Haystack property queryset serializer
    """

    id = serializers.IntegerField()
    name = serializers.CharField()
    locality = serializers.CharField()
    city = serializers.CharField()
    owner_name = serializers.SerializerMethodField()
    created = serializers.DateTimeField()
    total_price = serializers.CharField()
    expected_price = serializers.DecimalField(decimal_places=2, max_digits=20,required=False,  )
    monthly_rent = serializers.CharField()
    property_for = serializers.CharField()
    thumbnail_url = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    def get_coordinates(self, obj):
        return {
            'lat': obj.object.coordinates.y,
            'lng': obj.object.coordinates.x
        }

    def get_owner_name(self, obj):
        if obj.object.user:
            return obj.object.user.full_name
        return None

    def get_thumbnail_url(self, obj):
        images = obj.object.get_images.all()
        if images.exists():
            try:
                return images[0].image.url
            except:
                return None
        return None

    def get_slug(self, obj):
        return obj.object.slug

class MyPropertyListingSerializer(serializers.ModelSerializer):
    """ Property model serializer """
    num_of_views = serializers.SerializerMethodField()
    # num_of_responses = serializers.SerializerMethodField()
    completeness_data = serializers.SerializerMethodField()

    viewcount_graph_data = serializers.SerializerMethodField()
    clickcount_graph_data = serializers.SerializerMethodField()
    responsecount_graph_data = serializers.SerializerMethodField()


    class Meta:
        model = Property
        fields = (
            "id",
            "name",
            "property_for",
            "expected_price",
            "monthly_rent",
            "property_verified",
            "created",
            "num_of_views",
            "completeness_data",
            "slug",
            "viewcount_graph_data",
            "clickcount_graph_data",
            "responsecount_graph_data",
            "is_premium",
            "is_payment_expired",
            "property_verified",
        )

    def get_num_of_views(self, obj):
        views = obj.get_views.values("datestamp").annotate(count=Count("datestamp"))
        return views

    def get_num_of_responses(self, obj):
        views = obj.get_responses.values("datestamp").annotate(count=Count("datestamp"))
        return views

    def get_completeness_data(self, obj):
        return property_complete_percentage(obj)

    def get_viewcount_graph_data(self, obj):
        views = PropertyAnalytics.objects.filter(property__id=obj.id).values('month', 'year', 'view_count')
        return [{
                    "date": "%s %s"%(MONTHS_DICT[v['month']], v['year']),
                    "view": v['view_count']
                } for v in views]

    def get_clickcount_graph_data(self, obj):
        clicks = PropertyAnalytics.objects.filter(property__id=obj.id).values('month', 'year', 'click_count')
        return [{
                    "date": "%s %s"%(MONTHS_DICT[c['month']], c['year']),
                    "click": c['click_count']
                } for c in clicks]

    def get_responsecount_graph_data(self, obj):
        responses = PropertyAnalytics.objects.filter(property__id=obj.id).values('month', 'year', 'response_count')
        return [{
                    "date": "%s %s"%(MONTHS_DICT[r['month']], r['year']),
                    "response": r['response_count']
                } for r in responses]


class PropertyResponseSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving and creating Property responses.
    """

    class Meta:
        model = PropertyResponse
        fields = "__all__"


class FacilityTypeSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving facility types.
    """
    facilities = FacilitySerializer(many=True, read_only=True)

    class Meta:
        model = FacilityType
        fields = "__all__"


class PropertyReportSerializer(serializers.ModelSerializer):
    """
    serializer for creating property reports
    """

    class Meta:
        model = PropertyReport
        fields = "__all__"


class AdvertisementSerializer(serializers.ModelSerializer):
    """
    serializer for getting advertisement property
    """

    class Meta:
        model = Advertisement
        fields = "__all__"


class BannerListSerializer(serializers.ModelSerializer):
    """
    serializer for getting advertisement property
    """

    class Meta:
        model = Banner
        fields = "__all__"


class ActivityBasedSerializer(serializers.ModelSerializer):
    """
    serializer for getting activity popup data
    """

    class Meta:
        model = ActivityBasedPopup
        fields = "__all__"


class UserTimerSerializer(serializers.ModelSerializer):
    """
    serializer for getting user timer popup data
    """

    class Meta:
        model = UserTimerPopup
        fields = "__all__"