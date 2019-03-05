from django.db import models
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _

from utils.db import WynventPostgresDBBaseModel


class OurExperts(WynventPostgresDBBaseModel):

    """ Our Experts model """

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='advertisement',help_text="Upload image(.jpg,.png) of size less than 2MB")
    area_of_expert = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Expert')
        verbose_name_plural = _('Our Experts')

    def __str__(self):
        return self.name


class ExpertResponses(WynventPostgresDBBaseModel):

    """ Response regarding experts model """

    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), blank=True)
    message = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Expert Response')
        verbose_name_plural = _('Expert Responses')

    def __str__(self):
        return self.name+'-'+self.email

@receiver(post_save, sender=ExpertResponses, dispatch_uid="post_save_contest_entry")
def contest_entry_signal(instance, **kwargs):
    #need to change from email and subject
    created = kwargs['created']

    if created:
        email = EmailMessage('Expert Response', instance.message, to=[settings.ADMIN_EMAIL])
        email.send()
    else:
        pass

