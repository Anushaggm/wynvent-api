"""Author model for Zinnia"""
from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from zinnia.managers import EntryRelatedPublishedManager
from zinnia.managers import entries_published
from applications.blog.models import BlogAuthor

def safe_get_user_model():
    """
    Safe loading of the User model, customized or not.
    """
    user_app, user_model = settings.AUTHER_MODEL.split('.')
    return apps.get_registered_model(user_app, user_model)


class AuthorPublishedManager(models.Model):
    """
    Proxy model manager to avoid overriding of
    the default User's manager and issue #307.
    """
    published = EntryRelatedPublishedManager()

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Author(safe_get_user_model(),
             AuthorPublishedManager):
    """
    Proxy model around :class:`django.contrib.auth.models.get_user_model`.
    """

    def entries_published(self):
        """
        Returns author's published entries.
        """
        return entries_published(self.entries)

    @models.permalink
    def get_absolute_url(self):
        """
        Builds and returns the author's URL based on his username.
        """
        try:
            return super(Author, self).get_absolute_url()
        except AttributeError:
            return ('zinnia:author_detail', [self.get_username()])

    def __str__(self):
        """
        If the user has a full name, use it instead of the username.
        """
        return (self.first_name
                or self.last_name)

    class Meta:
        """
        Author's meta informations.
        """
        proxy = True