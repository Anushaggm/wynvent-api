from django.utils.translation import ugettext_lazy as _


WYNVENT_ADMIN = 'admin'

FB_GRAPH_API_PROFILE_URL = 'https://graph.facebook.com/me'

# Accounts
BUYER_OWNER = "buyer_owner"
AGENT = "agent"
BUILDER = "builder"
USER_TYPES = (
    (BUYER_OWNER, 'Buyer/Owner'),
    (AGENT, 'Agent'),
    (BUILDER, 'Builder'),
)

PROFILE_IMAGE_DIR = 'ProfileImage'
PROPERTY_IMAGE_DIR = 'PropertyImage'

# Property
PROPERTY_FOR_CHOICES = (
    ('sale', _('Sale')),
    ('rent', _('Rent')),
)
TRANSACTION_TYPES = (
    ('new_property', _('New Property')),
    ('resale', _('Resale'))
)
RESIDENTIAL_APARTMENT_PROPERTY_TYPE = "residential_apartment"
RESIDENTIAL_VILLA_PROPERTY_TYPE = "residential_villa"
COMMERCIAL_SHOWROOM_PROPERTY_TYPE = "commercial_showroom"
COMMERCIAL_SHOP_PROPERTY_TYPE = "commercial_shop"

PROPERTY_TYPES = (
    (RESIDENTIAL_APARTMENT_PROPERTY_TYPE, _("Residential Apartment")),
    (RESIDENTIAL_VILLA_PROPERTY_TYPE, _("Residential Villa")),
    (COMMERCIAL_SHOWROOM_PROPERTY_TYPE, _("Commercial Showroom")),
    (COMMERCIAL_SHOP_PROPERTY_TYPE, _("Commercial Shop"))
)
NON_FURNISHED_STATUS = "non_furnished"
SEMI_FURNISHED_STATUS = "semi_furnished"
FULLY_FURNISHED_STATUS = "fully_furnished"
FURNISHED_STATUS_CHOICES = (
    (NON_FURNISHED_STATUS, _("Non-Furnished")),
    (SEMI_FURNISHED_STATUS, _("Semi-Furnished")),
    (FULLY_FURNISHED_STATUS, _("Fully Furnished"))
)
AREA_UNITS = (
    ('sq_ft', 'Sq-ft'),
    ('sq_yrd', 'Sq-yrd'),
    ('sq_m', 'Sq-m'),
    ('acre', 'Acre'),
    ('hectare', 'Hectare'),
    ('ground', 'Ground'),
    ('cent', 'Cent'),
    ('are', 'Are')
)
CONSTRUCTION_AGE_CHOICES = (
    ('new_construction', _('New Construction')),
    ('less_than_5_years', _('Less than 5 years')),
    ('5_to_10_years', _('5 to 10 years')),
    ('10_to_15_years', _('10 to 15 years')),
    ('15_to_20_years', _('15 to 20 years')),
    ('above_20_years', _('Above 20 years')),
)
LENGTH_UNITS = (
    ('ft', 'ft'),
    ('yrd', 'yrd'),
    ('m', 'm'),
    ('Acre', 'Acre'),
    ('Bigha', 'Bigha'),
    ('Hectare', 'Hectare'),
    ('Marla', 'Marla'),
    ('Kanal', 'Kanal'),
    ('Biswa1', 'Biswa1'),
    ('Biswa2', 'Biswa2'),
    ('Ground', 'Ground'),
    ('Aankadam', 'Aankadam'),
    ('Rood', 'Rood'),
    ('Chatak', 'Chatak'),
    ('Kottah', 'Kottah'),
    ('Marla', 'Marla'),
    ('Cent', 'Cent'),
    ('Perch', 'Perch'),
    ('Guntha', 'Guntha'),
    ('Are', 'Are')
)
OWNERS_RESIDENCE_TYPES = (
    ('same_premise', _('Same premise')),
    ('away', _('Away')),
)
PANTRY_CHOICES = (
    ("dry", _("Dry")),
    ("wet", _("Wet")),
    ("not_available", _("Not Available"))
)
TENANT_RENT_CHOICES = (
    ("yes", _("Yes")),
    ("no", _("No")),
    ("does_not_matter", _("Doesn't Matter"))
)

# Import Property from external DB
MARKETING_PROPERTY_TYPE_LIST = [RESIDENTIAL_APARTMENT_PROPERTY_TYPE, RESIDENTIAL_VILLA_PROPERTY_TYPE, \
                                COMMERCIAL_SHOWROOM_PROPERTY_TYPE, COMMERCIAL_SHOP_PROPERTY_TYPE]
MARKETING_PROPERTY_SUBTYPE_LIST = ['Apartment', 'Villa', 'Showroom', 'Shop']
MARKETING_PROPERTY_SUBTYPE_MAPPINGS = [
    ('apartment', RESIDENTIAL_APARTMENT_PROPERTY_TYPE),
    ('villa', RESIDENTIAL_VILLA_PROPERTY_TYPE),
    ('showroom', COMMERCIAL_SHOWROOM_PROPERTY_TYPE),
    ('shop', COMMERCIAL_SHOP_PROPERTY_TYPE)
]

# Shortlist a property
ADD_TO_SHORTLIST = "add"
REMOVE_FROM_SHORTLIST = "remove"
PROPERTY_SHORTLIST_ACTIONS = (
    (ADD_TO_SHORTLIST, _('Add')),
    (REMOVE_FROM_SHORTLIST, _('Remove'))
)

# Property Sorting Choices
SORT_BY_PROXIMITY = "proximity"
SORT_BY_AGE_OF_CONSTRUCTION = "age_of_construction"

# Property Search
PROPERTY_SEARCH_DISTANCE = 25000  # In metres. Used for property filter.
BANNER_CHOICES = (
    ("normal_banner", _("Normal")),
    ("property_banner", _("Property")),
)
VALID_IMAGE_WIDTH = 1290
VALID_IMAGE_HEIGHT = 475

MONTHS = (
    (1, _('Jan')),
    (2, _('Feb')),
    (3, _('Mar')),
    (4, _('Apr')),
    (5, _('May')),
    (6, _('Jun')),
    (7, _('Jul')),
    (8, _('Aug')),
    (9, _('Sep')),
    (10, _('Oct')),
    (11, _('Nov')),
    (12, _('Dec')),
)

MONTHS_DICT = dict(MONTHS)

VIEW_COUNT = 'view_count'
CLICK_COUNT = 'click_count'
RESPONSE_COUNT = 'response_count'
PROXIMITY = 'proximity'


SORT_OPTIONS = (
    (VIEW_COUNT, _('View Count')),
    (CLICK_COUNT, _('Click Count')),
    (RESPONSE_COUNT, _('Response Count')),
    (PROXIMITY, _('Proximity'))
)

SORT_VAL_LIST = [VIEW_COUNT, CLICK_COUNT, RESPONSE_COUNT, PROXIMITY, 'contact_count']
