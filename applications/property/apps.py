from __future__ import unicode_literals

from django.apps import AppConfig


class PropertyConfig(AppConfig):
    name = 'property'

# from __future__ import unicode_literals
#
# from django.apps import AppConfig
# from django.db.models.signals import post_delete, post_save, m2m_changed
# from django.utils.translation import ugettext_lazy as _
#
# from utils.handlers import (
#     add_property_object_to_elastic_index,
#     generic_many_to_many_update_elastic,
#     delete_property_object_from_elastic_index
# )
#
#
# class PropertyConfig(AppConfig):
#     name = 'applications.property'
#     verbose_name = _('property')
#
#     def ready(self):
#         from applications.property.models import Property
#         post_delete.connect(delete_property_object_from_elastic_index, sender=Property)
#         post_save.connect(add_property_object_to_elastic_index, sender=Property)
#         m2m_changed.connect(generic_many_to_many_update_elastic, sender=Property.facilities.through)
