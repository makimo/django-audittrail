from django.conf import settings
from django.contrib import admin

from audittrail.models import Event


ENABLE_EVENT_ADMIN = getattr(settings, 'ENABLE_EVENT_ADMIN', False)

if ENABLE_EVENT_ADMIN:
    admin.site.register(Event)
