# utils/session_utils.py
from django.shortcuts import get_object_or_404
from authentication.models import Entreprise

def get_entreprise_active(request):
    entreprise_id = request.session.get("entreprise_active_id")
    if not entreprise_id:
        return None
    return get_object_or_404(Entreprise, id=entreprise_id)
