from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def role_required(roles):
    """
    Décorateur pour restreindre une vue à certains rôles.
    Usage :
        @role_required(["OWNER", "COMPTABLE"])
    """
    print('roles:', roles)
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # raise PermissionDenied("Vous devez être connecté.")
                return redirect("login")
            if request.user.has_role(*roles):
                return view_func(request, *args, **kwargs)
            # return redirect("forbidden")  # page 403 custom
            raise PermissionDenied("Accès interdit.")
        return _wrapped_view

    return decorator
