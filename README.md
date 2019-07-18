# Django-AuditTrail - Register and store users actions in database

This project allows tracking user actions within a Django powered system.

## Requirements

* python 3.6+
* Django 2.0+

## Installation

First install pip package using this command:

```
pip install django-audittrail
```

Then add audittrail to installed apps:

```
INSTALLED_APPS = [
    ...
    'django.contrib.contenttypes', # contenttypes app has to be included
    'audittrail',
]
```

Run migrations.

```
python manage.py migrate
```

## Basic usage

To register and create new event you have to attach `audit_trail` decorator to method or function.

It may look like this:
```
from audittrail.decorators import audit_trail

@audit_trail(description="Example")
def get(self, request, *args, **kwargs):
    ...
```

This will create new event everytime this view is invoked.
