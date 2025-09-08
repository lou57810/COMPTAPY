from django.core.exceptions import PermissionDenied

def role_required(roles):
    """
    Décorateur pour restreindre une vue à certains rôles.
    Exemple : @role_required(["OWNER", "COMPTABLE"])
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("Vous devez être connecté.")
            if request.user.role not in roles:
                raise PermissionDenied("Accès interdit pour votre rôle.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
