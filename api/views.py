from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from authentication.permissions import role_required
from django.contrib import messages
from authentication.forms import SignupForm
from .utils import create_user_and_entreprise
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FolderForm, EntrepriseForm, CompteForm
from .serializers import CompteComptableSerializer, EcritureJournalSerializer
from django.utils import timezone

from .models import CompteComptable, EcritureJournal, Entreprise
from django.db.models.functions import Substr

from rest_framework import generics, permissions

User = get_user_model()


"""
class CreateEntrepriseAPIView(generics.CreateAPIView):
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        # L’entreprise est liée à l’utilisateur connecté
        serializer.save(owner=self.request.user)
"""

def accueil_dossier_compta(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    entreprise_nom = None
    entreprise_gerant = None
    # entreprise_active = None

    if request.user.is_authenticated:
        # test = Entreprise.objects.filter(owner=request.user)
        entreprise_nom = entreprise.nom
        entreprise_gerant = entreprise.nom_gerant
        # entreprise_nom = test[0].nom
        # entreprise_gerant = test[0].nom_gerant
        # entreprise_active = getattr(request.user, "entreprise", None)
        # print('entreprise_gerant, test:', entreprise.nom, entreprise.nom_gerant)
    # On sauvegarde l'entreprise active dans la session
    # request.session["entreprise_active_id"] = entreprise.id
    request.session["entreprise_active_id"] = entreprise_id

    # if User.objects.filter(role="GERANT").exists():
    return render(request, "api/accueil_dossier_comptable.html", {"entreprise": entreprise, "entreprise_id": entreprise_id, "entreprise_nom": entreprise_nom, "entreprise_gerant": entreprise_gerant})

def liste_compte(request):
    return render(request, 'api/pgc.html', )


@login_required
def create_compte(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    entreprise_nom = entreprise.nom

    if request.method == 'POST':
        compte_form = CompteForm(request.POST)
        if compte_form.is_valid():
            compte = compte_form.save(commit=False)
            compte.entreprise = entreprise        # ✅ Lier explicitement
            compte.origine = 'user'               # ✅ Marquer comme créé par utilisateur
            compte.save()
            messages.success(request, 'Le compte a été créé avec succès !')
            return redirect('create-compte', entreprise_id=entreprise.id)
    else:
        compte_form = CompteForm()

    request.session["entreprise_active_id"] = entreprise_id
    return render(request, 'api/create_compte.html', {
        'compte_form': compte_form,
        'entreprise': entreprise,
        'entreprise_nom': entreprise_nom,
        'entreprise_id': entreprise_id
    })


from .models import CompteComptable, Entreprise
from django.shortcuts import render, get_object_or_404

def liste_compte_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    entreprise_nom = entreprise.nom

    # ✅ Filtrer les comptes appartenant uniquement à cette entreprise
    comptes = CompteComptable.objects.filter(entreprise=entreprise).order_by('numero')

    print(f"📊 {comptes.count()} comptes trouvés pour {entreprise_nom}")

    return render(
        request,
        'api/pgc_entreprise.html',
        {
            'entreprise': entreprise,
            'entreprise_nom': entreprise_nom,
            'entreprise_id': entreprise_id,
            'comptes': comptes,  # ✅ ajouter les comptes filtrés au contexte
        },
    )


def create_folder(request):
    role = request.GET.get("role")  # ignoré ici, on force GERANT
    if request.method == "POST":
        form = FolderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user, entreprise = create_user_and_entreprise(
                nom_gerant=data["nom_gerant"],
                email=data["email"],
                password=data["password1"],
                role="GERANT",   # ✅ fixé ici
                nom=data.get("nom"),
                siret=data.get("siret"),
                ape=data.get("ape"),
                adresse=data.get("adresse"),
                date_creation=data.get("date_creation"),
                owner=request.user if request.user.is_authenticated else None,
            )
            messages.success(request, f"L’entreprise '{entreprise.nom}' a été créée avec succès.")
            return redirect("accueil")
    else:
        form = FolderForm()

    return render(request, "api/ajouter_dossier.html", {"form": form})



@login_required
@role_required(["OWNER", "GERANT"])
def afficher_modifier_dossier(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    email = entreprise.owner.email

    if not entreprise:
        return redirect("créer_dossier")

    if request.method == "POST":
        form = EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            entreprise.owner.email = form.cleaned_data["email"]
            entreprise.owner.save(update_fields=["email"])
            # return redirect("afficher-statuts", entreprise_id=entreprise_id)
            return redirect("liste-entreprises")
    else:
        form = EntrepriseForm(instance=entreprise, initial={
        "email": entreprise.owner.email if entreprise.owner else ""
    })
    return render(request, "api/afficher_statuts.html", {"form": form, "entreprise": entreprise})


@login_required
def supprimer_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)

    # Vérifie si l'utilisateur connecté est bien le propriétaire
    print("Request_user_role", request.user.role, "entreprise_owner_email", entreprise.owner, "request_user", request.user)
    # reponse requestuserrole = owner
    # entrepriseowner = test@localhost
    # request.user = ben@localhost
    if request.user.role == "OWNER": # and entreprise.owner == request.user:
        owner = entreprise.owner  # sauvegarde avant suppression
        entreprise.delete()
        messages.success(request, f"L'entreprise '{entreprise.nom}' a été supprimée.")
        """
        # Vérifie si c'était la dernière entreprise de ce propriétaire
        if not Entreprise.objects.filter(owner=owner).exists():
            owner.delete()  # supprime le compte propriétaire
            messages.info(request, "Le compte propriétaire a été supprimé car il n'avait plus d'entreprises.")
            return redirect("signup")  # retour vers l'écran d'inscription
        else:
        """
        return redirect("liste-entreprises")

    else:
        messages.error(request, "Action non autorisée.")
        return redirect("liste-entreprises")



class CompteComptableViewSet(viewsets.ModelViewSet):
    serializer_class = CompteComptableSerializer

    # Tri numéro PGC en fonction des 3 premiers chiffres
    def get_queryset(self):
        return CompteComptable.objects.annotate(
            numero_prefix=Substr('numero', 1, 3)
        ).order_by('numero_prefix', 'numero')

    def perform_create(self, serializer):
        serializer.save(origine='user')


# @login_required
class CompteComptableListView(generics.ListAPIView):
    serializer_class = CompteComptableSerializer

    # Tri numéro PGC en fonction des 3 premiers chiffres
    def get_queryset(self):
        return CompteComptable.objects.annotate(
            numero_prefix=Substr('numero', 1, 6)
        ).order_by('numero_prefix', 'numero')


class CompteComptableRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompteComptable.objects.all()
    serializer_class = CompteComptableSerializer
    lookup_field = "pk"


@api_view(['GET'])
def get_compte_by_numero(request):
    numero = request.GET.get('numero')
    # if numero is None:
    if not numero:
        return Response({'error': 'Numéro manquant'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        compte = CompteComptable.objects.get(numero=numero)
        serializer = CompteComptableSerializer(compte)
        return Response(serializer.data)
    except CompteComptable.DoesNotExist:
        return Response({'error': 'Compte introuvable'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def enregistrer_ecritures(request):
    lignes = request.data.get('lignes', [])

    for ligne in lignes:
        numero = ligne.get('numero')
        nom = ligne.get('nom')
        numero_piece = ligne.get('numero_piece')
        libelle = ligne.get('libelle') or ''
        debit = ligne.get('debit') or 0
        credit = ligne.get('credit') or 0

        CompteComptable.objects.create(
            numero=numero,
            nom=nom,
            numero_piece=numero_piece,
            libelle=libelle,
            debit=debit,
            credit=credit,
            date_saisie=timezone.now()
        )

    return Response({'message': 'Écritures enregistrées'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_ecritures_par_compte(request):
    numero = request.GET.get('numero')

    if numero:
        ecritures = EcritureJournal.objects.filter(compte__numero=numero).order_by('date')

        data = [
            {
                'date': ecriture.date.strftime('%d/%m/%Y'),
                'numero': ecriture.compte.numero,
                'nom': ecriture.nom,
                'numero_piece': ecriture.numero_piece,
                'libelle': ecriture.libelle,
                'debit': ecriture.debit,
                'credit': ecriture.credit
            }
            for ecriture in ecritures
        ]

        return Response(data, status=status.HTTP_200_OK)

    return Response({'message': 'Numéro de compte manquant'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ecritures_par_compte(request):
    numero = request.GET.get('numero')
    if numero:
        ecritures = EcritureJournal.objects.filter(compte__numero=numero).order_by('date')
        serializer = EcritureJournalSerializer(ecritures, many=True)
        return Response(serializer.data)
    return Response({'error': 'Numéro de compte requis'}, status=400)



