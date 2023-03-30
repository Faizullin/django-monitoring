from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin


from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


def owner_required(model, id_field='id', owner_field='owner'):
    """
    Decorator for views that checks that the authenticated user is the owner of
    the specified model instance.
    
    Usage: 
    @owner_required(MyModel)
    def my_view(request, my_model_id):
        # ...
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            instance = get_object_or_404(model, **{id_field: kwargs[id_field]})
            if not getattr(instance, owner_field) == request.user:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


class OwnerRequiredMixin(UserPassesTestMixin):
    """
    Mixin to require a user to be in a specific group.
    """
    group_required = "shop-owner"

    def test_func(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name=self.group_required).exists():
            return True
        return False

def group_required(group_names):
    """
    Decorator that checks if the user belongs to at least one of the specified
    groups. If not, redirects to the login page or raises a PermissionDenied
    exception, depending on the `login_url` and `raise_exception` arguments.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrapper
    return decorator