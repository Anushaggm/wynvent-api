from haystack import indexes

from applications.property.models import Property


class PropertyIndex(indexes.SearchIndex, indexes.Indexable):
    id = indexes.IntegerField(model_attr='pk', indexed=False)
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    # owner_name = indexes.CharField()
    total_price = indexes.DecimalField(model_attr="total_price", null=True)
    bedroom_count = indexes.IntegerField(model_attr="bedroom_count", null=True)
    bathroom_count = indexes.IntegerField(model_attr="bathroom_count", null=True)
    puja_room = indexes.BooleanField(model_attr="puja_room", null=True)
    study_room = indexes.BooleanField(model_attr="study_room", null=True)
    store_room = indexes.BooleanField(model_attr="store_room", null=True)
    property_for = indexes.CharField(model_attr="property_for", null=True)
    type = indexes.CharField(model_attr="type", null=True)
    locality = indexes.CharField(model_attr='locality', null=True)
    city = indexes.CharField(model_attr='city', null=True)
    zipcode = indexes.CharField(model_attr='zipcode', null=True)
    maintenance_charges = indexes.BooleanField(model_attr="maintenance_charges", null=True)
    security_deposit = indexes.IntegerField(model_attr="security_deposit", null=True)
    plot_area = indexes.DecimalField(model_attr="plot_area", null=True)
    user_type = indexes.CharField(model_attr='user__type', null=True)
    rent_to_bachelors = indexes.CharField(model_attr="rent_to_bachelors", null=True)
    rent_to_family = indexes.CharField(model_attr="rent_to_family", null=True)
    rent_to_non_vegetarians = indexes.CharField(model_attr="rent_to_non_vegetarians", null=True)
    rent_to_with_pets = indexes.CharField(model_attr="rent_to_with_pets", null=True)
    facilities = indexes.MultiValueField()
    location = indexes.LocationField(model_attr='coordinates', null=True)
    created = indexes.DateTimeField(model_attr="created")
    monthly_rent = indexes.DecimalField(model_attr='monthly_rent', null= True)
    expected_price = indexes.IntegerField(model_attr='expected_price', null= True)
    # thumbnail_url = indexes.CharField()

    # Analytics
    view_count = indexes.IntegerField(model_attr='view_count', null=True)
    click_count = indexes.IntegerField(model_attr='click_count', null=True)
    response_count = indexes.IntegerField(model_attr='response_count', null=True)

    # AutoComplete Fields
    name_auto = indexes.EdgeNgramField(model_attr='name')
    name_search = indexes.NgramField()

    def get_model(self):
        return Property

    def index_queryset(self, using=None):
        return self.get_model().objects.select_related('user').prefetch_related(
            "get_images", "facilities").all()

    def prepare_owner_name(self, obj):
        return obj.user.full_name

    def prepare_facilities(self, obj):
        return [prop.name for prop in obj.facilities.all()]

    def prepare_thumbnail_url(self, obj):
        images = obj.get_images.all()
        if images.exists():
            try:
                return images[0].image.url
            except:
                return None
        return None
