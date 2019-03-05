# coding=utf-8

from haystack import connections


def update_elastic(model, instance, using, process_type='update'):
    index = connections[using].get_unified_index().get_index(model)
    if process_type == 'update':
        index.update_object(instance, using=using)

    if process_type == 'remove':
        index.remove_object(instance, using=using)


def add_property_object_to_elastic_index(sender, **kwargs):
    instance = kwargs.pop('instance')
    update_elastic(sender, instance, 'default')


def generic_many_to_many_update_elastic(sender, **kwargs):
    instance = kwargs.pop('instance')
    update_elastic(type(instance), instance, 'default')


def delete_property_object_from_elastic_index(sender, **kwargs):
    instance = kwargs.pop('instance')
    update_elastic(sender, instance, 'default', process_type='remove')
