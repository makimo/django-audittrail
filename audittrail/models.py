from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    """
    Stores all events done by user in application.
    """
    user_id = models.PositiveIntegerField(verbose_name=_('User ID'), null=True, blank=True)
    """User ID, null when user made actions but was not logged in."""

    user_description = models.CharField(verbose_name=_('User description'), default='',
        max_length=255)
    """User description."""

    ip_addr = models.GenericIPAddressField(verbose_name=_('IP address'))
    """The IP address of the client."""

    event_time = models.DateTimeField(auto_now=True)
    """Date and time when event was created."""

    request_path = models.URLField(verbose_name=_('Request path'))
    """URL of called request."""

    event_description = models.TextField(verbose_name=_('Event description'))
    """Description of event/action done by user."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()
    """
    GenericForeignKey was used to attach audit trail events to any object in the system.
    """
