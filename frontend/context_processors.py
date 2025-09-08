from api.models import Entreprise

def entreprise_context(request):
    return {
        "entreprise_exist": Entreprise.objects.exists()
    }
