from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from utils.db import WynventPostgresDBBaseModel
from applications.locations.models import City

class Blog(WynventPostgresDBBaseModel):

    """ Blog model """

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey("BlogAuthor", null=True)
    cover_photo = models.ImageField(upload_to="blog/")
    type = models.ForeignKey("BlogType", null=True)
    slug = AutoSlugField(populate_from='title')

    def __str__(self):
        return self.title


class BlogAuthor(WynventPostgresDBBaseModel):

    """ Blog Author model """

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to="blog/author/")
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    facebook_url = models.CharField(_('Facebook URL'), max_length=255, blank=True)
    twitter_url = models.CharField(_('Twitter URL'), max_length=255, blank=True)
    gplus_url = models.CharField(_('Google+ URL'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('Blog Author')
        verbose_name_plural = _('Blog Authors')

    def __str__(self):
        return self.first_name


class BlogType(WynventPostgresDBBaseModel):

    """ Blog Type model """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Blog Type')
        verbose_name_plural = _('Blog Types')

    def __str__(self):
        return self.name


class BlogImage(WynventPostgresDBBaseModel):

    """ Blog Image model """

    image = models.ImageField(upload_to="blog/")
    blog = models.ForeignKey(Blog, related_name="get_images", null=True)

    class Meta:
        verbose_name = _('Blog Image')
        verbose_name_plural = _('Blog Images')

    def __str__(self):
        return self.image.url


class BlogView(models.Model):
    """
    Views under a blog
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, related_name="get_views", null=True)

    class Meta:
        verbose_name = _('Blog View')
        verbose_name_plural = _('Blog Views')

    def __str__(self):
        return "%s : %s" % (self.timestamp, self.blog.title)


class TalkToExpert(WynventPostgresDBBaseModel):

    """ Blog Talk to expert model """

    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), blank=True)
    message = models.TextField(blank=True)
    city = models.ForeignKey(City,null=True)

    class Meta:
        verbose_name = _('Talk To Expert')
        verbose_name_plural = _('Talk To Expert')

    def __str__(self):
        return self.name
