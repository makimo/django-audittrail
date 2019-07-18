# Basic usage

To use `audit_trail` decorator you have to import it first:

```python
from audittrail.decorators import audit_trail
```

### Class-Based Views

Decorator with simple `description`:
```python
class Example(View):
    @audit_trail(description="Example")
    def get(self, request, *args, **kwargs):
        ...
```

Decorator which uses lambda function to specify `description`:
```python
class Example(View):
    @audit_trail(description=lambda self, request, pk: 'Example on {}'.format(request.path))
    def post(self, request, pk):
        ...
```

Decorator with functions to specify `description` and `object` when form is valid:
```python
class Example(CreateView):
    ...

    def make_description_example(request, form):
        return 'Example on {}'.format(request.path)

    def make_object_example(request, form):
        return form.save(commit=False)

    @audit_trail(description=make_description_example, object=make_object_example)
    def form_valid(self, form):
        ...
```

### Function-Based Views

Decorator with lambda function to specify `description`: 
```python
@audit_trail(description=lambda request: 'Example on {}'.format(request.path))
def example_view(request):
    ...
```

Decorator with lambda function to specify `description` with additional parameter: 
```python
@audit_trail(description=lambda request, pk: 'Example on {}-{}'.format(request.path, pk))
def example_view(request, pk):
    ...
```

Decorator with string `description` and lambda function to specify `object`: 
```python
@audit_trail(description="Example", object=lambda request: Event.objects.first())
def example_view(request):
    ...
```
