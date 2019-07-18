# API documentation

## Event model

Event is a main class used by `django-audittrail` to store events in database for your application.
This model contains the following fields:

`user_id`

* type: PositiveIntegerField
* required: False
* description: ID from `User` model.


`user_description`

* type: CharField
* required: True
* default: `''`
* description: `User` description.


`ip_addr`

* type: GenericIPAddressField
* required: True
* description: The IP address of the client.


`event_time`

* type: DateTimeField
* required: True
* auto_now: True
* description: Date when event was created.


`request_path`

* type: URLField
* required: True
* description: URL of called request.


`event_description`

* type: TextField
* required: True
* description: Description of action done by user.


`content_object`

* type: GenericForeignKey
* required: False
* description: `GenericForeignKey` was used to attach audit trail events to any object in the system.

By default `Event` model is not registered in Django admin site. To enable edition set `ENABLE_EVENT_ADMIN`
to `True` in your Django settings module.

## audit_trail decorator

To use `audit_trail` decorator you have to import it like this:

```python
from audittrail.decorators import audit_trail
```

`audit_trail` decorator accepts two parameters:

* description (required) - This parameter is used to specify `event_description` field for new `Event` object. To do this you can use string or function.

Examples:

```python
@audit_trail(description='Example')
def example(request):
    ...
```

```python
@audit_trail(description=lambda request: 'Example on {}'.format(request.path))
def example(request):
    ...
```

* object (optional) - Callback to add any Model object from your application into `content_object` inside `Event` model.

Example:

```python
@audit_trail(description='Example', object=lambda request: Event.objects.first())
def example(request):
    ...
```

If you don't want to use decorator, you can log your events manuall with log_event function:

```python
from audittrail.utils import log_event
```

This function takes three arguments:

* request (required) - Request object.
* description (required) - This parameter is used to specify `event_description` field for new `Event` object. To do this you can use either string or function.
* object (optional) - Callback to add any Model object from your application into `content_object` inside `Event` model.

Example:

```python
log_event(request, "Example", lambda request: Event.objects.first())
```
