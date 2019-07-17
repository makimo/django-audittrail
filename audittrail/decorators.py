import types
from typing import Optional, Union

from .utils import log_event


class audit_trail(object):
    """
    Decorator responsible for creating `Event` object when marked view is requested.

    Args:
        description (required)- It specifies `event_description` field for `Event` object.
            It can be string, callable function or ugettext_lazy.
            It requires to have request as first parameter when using as callable.
        object (optional) - Callback to generate `content_object` foreign key.

    Usage examples:
        @audit_trail(description="Example")
        def get(self, request, *args, **kwargs):
            ...

        @audit_trail(description=lambda request: 'Example on {}'.format(request.path))
        def get(request):
            ...

        @audit_trail(description=lambda request, pk: 'Example on {}-{}'.format(request.path, pk))
        def get(request, pk):
            ...

        @audit_trail(description="Example", object=lambda request: Event.objects.first())
        def post(request):
            ...
    """

    def __init__(self, *args, **kwargs):
        self.description = kwargs.get('description', None)
        self.object = kwargs.get('object', None)

    def __call__(self, f):
        def wrap(request, *args, **kwargs):
            value = f(request, *args, **kwargs)
            request_wsgi = _get_request(request)
            log_event(request_wsgi, self.description, self.object, *args, **kwargs)
            return value

        return wrap


def _get_request(request: 'Request') -> 'Request':
    """
    Gets request object depending on type of view i.e
    class-based-view or function-based-view.
    """
    if 'request' in request.__dict__:
        return request.request
    else:
        return request
