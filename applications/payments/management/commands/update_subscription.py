import datetime as dt

from django.utils import timezone
from django.core.management.base import BaseCommand

# if email has to send in future
# from django.core.mail import EmailMessage
# from django.template import Context, loader

from applications.property.models import Property
from applications.agent.models import Agent
from applications.builder.models import Builder


class Command(BaseCommand):
    """
    For each subscription check expired or not
    """

    def handle(self, *args, **options):
        subscribed_properties = Property.objects.all().exclude(is_payment_expired=True)
        subscribed_agents = Agent.objects.all().exclude(expired=True)
        subscribed_builders = Builder.objects.all().exclude(expired=True)
        today = dt.datetime.today().strftime("%Y-%m-%d")
        for property in subscribed_properties:
            #for premium or standard properties
            if property.is_premium:
                get_one_twenty_day = property.payment_created + timezone.timedelta(days=120)
                if get_one_twenty_day.date() == today:
                    property.is_payment_expired = True
                    property.is_premium = False
                    property.save()
            if property.is_standard:
                get_sixty_day = property.payment_created + timezone.timedelta(days=60)
                if get_sixty_day == today:
                    property.is_payment_expired = True
                    property.is_standard = False
                    property.save()
                else:
                    pass
        for agent in subscribed_agents:
            #for premium or standard agent
            if agent.premium:
                get_one_twenty_day = agent.payment_created + timezone.timedelta(days=120)
                if get_one_twenty_day == today:
                    agent.expired = True
                    agent.premium = False
                    agent.save()
            if agent.standard:
                get_sixty_day = agent.payment_created + timezone.timedelta(days=60)
                if get_sixty_day == today:
                    agent.expired = True
                    agent.is_standard = False
                    agent.save()
                else:
                    pass
        for builder in subscribed_builders:
            #for premium or standard builder
            if builder.premium:
                get_one_twenty_day = builder.payment_created + timezone.timedelta(days=120)
                if get_one_twenty_day == today:
                    builder.expired = True
                    builder.premium = False
                    builder.save()
            if builder.standard:
                get_sixty_day = builder.payment_created + timezone.timedelta(days=60)
                if get_sixty_day == today:
                    builder.expired = True
                    builder.is_standard = False
                    builder.save()
                else:
                    pass