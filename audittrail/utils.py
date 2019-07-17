import types
from typing import Any, Optional, Union

from django.utils.translation import ugettext_lazy as _ 

from .models import Event


def log_event(request: 'Request', description: Union[str, types.FunctionType],
    object: Optional[types.FunctionType] = None, *args, **kwargs) -> None:
    """Creates new `Event` object.
    
    Args:
        description - It specifies `event_description` field for `Event` object.
            It can be string, callable function or ugettext_lazy.
        object - Callback to generate `content_object` foreign key.
    """
    event_data = dict(
        ip_addr=request.META['REMOTE_ADDR'],
        request_path=request.path,
        event_description=_get_event_description(request, description, *args, **kwargs)
    )

    if object:
        event_data['content_object'] = _get_object(object, request, *args, **kwargs)

    if request.user:
        event_data.update({
            'user_id': request.user.id,
            'user_description': str(request.user)
        })

    Event.objects.create(**event_data)


def _get_event_description(request: 'Request', description:
    Union[str, types.FunctionType], *args, **kwargs) -> str:
    """
    Gets `event_description` from lambda, str or ugettext_lazy `description` parameter.

    Args:
        description - Description sent to decorator.

    Returns:
        str - Description as string.

    Raises:
        TypeError - When description argument has other type than
        `str` or `types.FunctionType`.
    """
    if isinstance(description, types.FunctionType):
        return description(request, *args, **kwargs)

    if isinstance(description, str):
        return description

    if isinstance(description, type(_(''))):
        return str(description)

    raise TypeError(_("Parameter description has wrong type."
        "Only <'function'> and <'str'> are supported"))


def _get_object(object: Any, request, *args, **kwargs):
    """Gets object instance for 'object_callable` property.
    
    Args:
        object: Callable function or any object in system.
    """
    if isinstance(object, types.FunctionType):
        return object(request, *args, **kwargs)
    else:
        return object
