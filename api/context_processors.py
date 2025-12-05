from .models import Entreprise

def entreprise_context(request):
    # return {
        # "entreprise_exist": Entreprise.objects.exists()
    # }
    """Injecte automatique l’entreprise du user connecté dans tous les templates."""
    if not request.user.is_authenticated:
        return {}

    # Entreprise où le user est GERANT
    entreprise = Entreprise.objects.filter(gerant=request.user).first()

    # Sinon entreprise où il est OWNER
    if not entreprise:
        entreprise = Entreprise.objects.filter(owner=request.user).first()

    return {
        "entreprise_exist": Entreprise.objects.exists(),
        "entreprise": entreprise,
        "entreprise_id": entreprise.id if entreprise else None
    }
