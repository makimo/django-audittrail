# django-audittrail

This project allows tracking user actions within a Django powered system.
You can assign any model entity you created in your application to `content_object` which uses `GenericForeignKey` field. In addition it contains `user_id` field which is not related
to the basic `User` model so you can assign id of user, regardless of `User` instance you use.

## Requirements
  
* python 3.6+
* Django 2.0+

django-audittrail may as well work on previous versions of Django and Python, however it has not yet been tested.

## Installation

First install pip package using this command:

```python
pip install django-audittrail
```

Then add audittrail to installed apps

```python
INSTALLED_APPS = [
    ...
    'django.contrib.contenttypes', # contenttypes app has to be included
    'audittrail',
]
```

Run migrations to create `Event` model.

```python
python manage.py migrate
```

By default `Event` model is not registered in Django admin site. To enable edition set `ENABLE_EVENT_ADMIN`
to `True` in your Django settings module.


## Contents
* [Usage](/usage/)
* [API documentation](/api/)
* [License](/license/)
