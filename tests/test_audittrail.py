import pytest

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.test import RequestFactory
from django.views import View
from django.views.generic.edit import CreateView

from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import booleans, composite, dictionaries, integers, text, tuples
from string import printable

from audittrail.decorators import audit_trail
from audittrail.models import Event


"""Those views are used only for testing purposes."""

@audit_trail(description="Test")
def string_view(request):
    return HttpResponse()


@audit_trail(description=lambda request: 'Test on {}'.format(request.path))
def lambda_view(request):
    return HttpResponse()


class ClassTestView(View):
    @audit_trail(description="Test")
    def get(self, request, *args, **kwargs):
        return HttpResponse()


class ClassTestViewWithPK(View):
    @audit_trail(description=lambda self, request, pk: 'Test on {} with {}'.format(request.path, pk),
        object=lambda self, request, pk: User.objects.get(pk=pk))
    def get(self, request, pk):
        return HttpResponse()


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = '/test'

    @audit_trail(description=lambda self, form: 'Test on {}'.format(self.path),
        object=lambda self, form: form.save(commit=False))
    def form_valid(self, form):
        return super().form_valid(form)


class AuditTrailTestCase(TestCase):
    """TestCase for audit_trail decorator class."""

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_audit_trail_string_not_logged_function_view(self):
        """
        Test if event was created for string description, function-based-view,
        without logged in user.
        """
        events_before = Event.objects.count()

        request = self.factory.get('/test')
        request.user = None
        response = string_view(request)

        assert response.status_code == 200
        assert events_before + 1 == Event.objects.count()

        event = Event.objects.last()

        assert event.event_description == "Test"
        assert event.user_id == None
        assert event.user_description == ''
        assert event.request_path == '/test'

    def test_audit_trail_string_logged_user_function_view(self):
        """
        Test if event was created for string description, function-based-view,
        with logged user.
        """
        user = User.objects.create_superuser('test', 'test@test.pl', 'secret')
        events_before = Event.objects.count()

        request = self.factory.get('/test')
        request.user = user
        response = string_view(request)

        assert response.status_code == 200
        assert events_before + 1 == Event.objects.count()

        event = Event.objects.last()

        assert event.event_description == "Test"
        assert event.user_id == user.id
        assert event.user_description == str(user)
        assert event.request_path == '/test'

    def test_audit_trail_string_function_class(self):
        """
        Test if event was created for string description, class-based-view.
        """
        user = User.objects.create_superuser('test', 'test@test.pl', 'secret')
        events_before = Event.objects.count()

        request = self.factory.get('/test')
        request.user = user
        response = ClassTestView.as_view()(request)

        assert response.status_code == 200
        assert events_before + 1 == Event.objects.count()

        event = Event.objects.last()

        assert event.event_description == "Test"
        assert event.user_id == user.id
        assert event.user_description == str(user)
        assert event.request_path == '/test'

    def test_audit_trail_string_logged_user_class_view(self):
        """
        Test if event was created for string description, class-based-view,
        with logged user.
        """
        user = User.objects.create_superuser('test', 'test@test.pl', 'secret')
        events_before = Event.objects.count()

        request = self.factory.get('/test')
        request.user = user
        response = ClassTestView.as_view()(request)

        assert response.status_code == 200
        assert events_before + 1 == Event.objects.count()

        event = Event.objects.last()

        assert event.event_description == "Test"
        assert event.user_id == user.id
        assert event.user_description == str(user)
        assert event.request_path == '/test'

    def test_audit_trail_lambda_not_logged_function_view(self):
        """
        Test if event was created for lambda description, function-based-view,
        without logged in user.
        """
        events_before = Event.objects.count()

        request = self.factory.get('/test')
        request.user = None
        response = lambda_view(request)

        assert response.status_code == 200
        assert events_before + 1 == Event.objects.count()

        event = Event.objects.last()

        assert event.event_description == 'Test on /test'
        assert event.user_id == None
        assert event.user_description == ''
        assert event.request_path == '/test'

    def test_audit_trail_lambda_logged_user_function_view(self):
        """
        Test if event was created for lambda description, function-based-view,
        with logged user.
        """
        user = User.objects.create_superuser('test', 'test@test.pl', 'secret')
        events_before = Event.objects.count()

        request = self.factory.get('/test')
        request.user = user
        response = lambda_view(request)

        assert response.status_code == 200
        assert events_before + 1 == Event.objects.count()

        event = Event.objects.last()

        assert event.event_description == 'Test on /test'
        assert event.user_id == user.id
        assert event.user_description == str(user)
        assert event.request_path == '/test'

    def test_audit_trail_int_logged_user_function_view_raise_type_error(self):
        """
        Test if event wasn't created for int description and TypeError was raised.
        """
        @audit_trail(description=1)
        def int_view(request):
            return HttpResponse()

        user = User.objects.create_superuser('test', 'test@test.pl', 'secret')
        events_before = Event.objects.count()

        request = self.factory.get('/test')
        request.user = user
        with self.assertRaises(TypeError):
            response = int_view(request)
        
        assert events_before == Event.objects.count()

    def test_audit_trail_description_none(self):
        """
        Test if event wasn't created for None description and TypeError was raised.
        """
        @audit_trail(description=None)
        def none_view(request):
            return HttpResponse()

        events_before = Event.objects.count()

        request = self.factory.get('/test')
        request.user = None

        with self.assertRaises(TypeError):
            response = none_view(request)

        assert events_before == Event.objects.count()

    def test_audit_trail_string_not_logged_function_view_with_argument(self):
        """
        Test if event was created for string description, function-based-view with args,
        without logged in user.
        """
        @audit_trail(description="Test")
        def with_url_argument_view(request, pk):
            return HttpResponse()

        events_before = Event.objects.count()

        request = self.factory.get('/test')
        request.user = None
        response = with_url_argument_view(request, 1)

        assert response.status_code == 200
        assert events_before + 1 == Event.objects.count()

        event = Event.objects.last()

        assert event.event_description == 'Test'
        assert event.user_id == None
        assert event.user_description == ''
        assert event.request_path == '/test'

    def test_audit_trail_with_object(self):
        """Check if `content_object` was created for `Event`."""
        @audit_trail(description="Test", object=lambda request: Event.objects.last())
        def with_object_view(request):
            return HttpResponse()

        request = self.factory.get('/test')
        request.user = None
        response = string_view(request)

        request = self.factory.get('/test')
        request.user = None
        response = with_object_view(request)

        event = Event.objects.last()

        assert event != None
        assert event.content_object != None

    def test_audit_trail_with_pk_in_request(self):
        """Test if decorator works with additional arguments in view."""
        @audit_trail(description=lambda request, pk: '{}'.format(request.path),
            object=lambda request, pk: Event.objects.filter(user_id=pk).first())
        def request_with_pk(request, pk, *args, **kwargs):
            return HttpResponse()

        user = User.objects.create_superuser('test', 'test@test.pl', 'secret')

        request = self.factory.get('/test')
        request.user = user
        response = string_view(request)
        event1 = Event.objects.last()

        request = self.factory.get('/test')
        request.user = user
        response = request_with_pk(request, user.pk)
        event2 = Event.objects.last()

        assert event2 != None
        assert event2.content_object == event1

    @composite
    def random_args(draw):
        return draw(tuples(integers(), booleans(), text(printable)))

    @composite
    def random_kwargs(draw):
        return draw(dictionaries(text(printable), integers() | booleans() | text(printable)))

    @given(random_args(), random_kwargs())
    def test_audit_trail_spy(self, generated_args, generated_kwargs):
        """Test args and kwargs are same like in view for `description`."""
        user = User.objects.create_superuser('test', 'test@test.pl', 'secret')

        def spy(request, *args, **kwargs):
            assert args == generated_args
            assert kwargs == generated_kwargs
            return "TEST"

        @audit_trail(description=spy)
        def view(request, *args, **kwargs):
            return HttpResponse()

        request = self.factory.get('/test')
        request.user = user
        response = view(request, *generated_args, **generated_kwargs)

    @given(random_args(), random_kwargs())
    def test_audit_trail_spy_object(self, generated_args, generated_kwargs):
        """Test args and kwargs are same like in view for `object`."""
        user = User.objects.create_superuser('test', 'test@test.pl', 'secret')

        def spy(request, *args, **kwargs):
            assert args == generated_args
            assert kwargs == generated_kwargs
            return User.objects.last()

        @audit_trail(description="Example", object=spy)
        def view(request, *args, **kwargs):
            return HttpResponse()

        request = self.factory.get('/test')
        request.user = user
        response = view(request, *generated_args, **generated_kwargs)

    @given(random_args(), random_kwargs())
    def test_audit_trail_spy_object_and_description(self,
        generated_args, generated_kwargs):
        """
        Test args and kwargs are same like in view for
        when both `description` and `object` are used with functions.
        """
        user = User.objects.create_superuser('test', 'test@test.pl', 'secret')

        def spy(request, *args, **kwargs):
            assert args == generated_args
            assert kwargs == generated_kwargs
            return "TEST"

        def spy2(request, *args, **kwargs):
            assert args == generated_args
            assert kwargs == generated_kwargs
            return User.objects.last()

        @audit_trail(description=spy, object=spy2)
        def view(request, *args, **kwargs):
            return HttpResponse()

        request = self.factory.get('/test')
        request.user = user
        response = view(request, *generated_args, **generated_kwargs)

    def test_audit_trail_string_function_class_with_pk(self):
        """
        Test if event was created for string description, class-based-view with pk.
        """
        user = User.objects.create_superuser('test', 'test@test.pl', 'secret')
        events_before = Event.objects.count()

        request = self.factory.get('/test/{}'.format(user.pk))
        request.user = user
        response = ClassTestViewWithPK.as_view()(request, user.pk)

        assert response.status_code == 200
        assert events_before + 1 == Event.objects.count()

        event = Event.objects.last()

        assert event.event_description == 'Test on /test/{0} with {0}'.format(user.pk)
        assert event.user_id == user.id
        assert event.user_description == str(user)
        assert event.request_path == '/test/{}'.format(user.pk)
        assert event.content_object == user

    def test_audit_trail_string_function_class_with_form(self):
        """
        Test if event was created for string description, class-based-view with form.
        """
        user_data = {
            'username': 'test',
            'email': 'test@test.pl',
            'password1': 'secret123#',
            'password2': 'secret123#'
        }

        events_before = Event.objects.count()

        request = self.factory.post('/test', user_data)
        request.user = None
        response = UserCreateView.as_view()(request)

        assert response.status_code == 302
        assert events_before + 1 == Event.objects.count()

        event = Event.objects.last()

        assert event.event_description == 'Test on /test'
        assert event.user_id == None
        assert event.request_path == '/test'
