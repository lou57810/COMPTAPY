from django.shortcuts import render
from .models import EcritureJournal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json




def journal_achats(request):
    return render(request,'journaux/journal_achats.html')


def journal_ventes(request):
    return render(request,'journaux/journal_ventes.html')


def journal_od(request):
    return render(request,'journaux/journal_od.html')


def journal_banque(request):
    return render(request,'journaux/journal_banque.html')


def journal_caisse(request):
    return render(request,'journaux/journal_caisse.html')


def journal_cpte_cheques_postaux(request):
    return render(request,'journaux/journal_cpte_cheques_postaux.html')


def journal_effets_a_payer(request):
    return render(request,'journaux/journal_effets_a_payer.html')


def journal_effets_a_recevoir(request):
    return render(request,'journaux/journal_effets_a_recevoir.html')


def journal_report_nouveau(request):
    return render(request,'journaux/journal_report_nouveau.html')


def journal_cloture(request):
    return render(request,'journaux/journal_cloture.html')


def journal_expert_od(request):
    return render(request,'journaux/journal_expert_od.html')


def journal_reouverture(request):
    return render(request,'journaux/journal_reouverture.html')

def journal_type(request):
    return render(request,'journaux/journal_type.html')

@csrf_exempt  # Si tu n'utilises pas {% csrf_token %}, sinon retire ça
def valider_journal_achats(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lignes = data.get('lignes', [])

            for ligne in lignes:
                date, compte, nom, libelle, quantite, taux, debit, credit, journal = ligne

                # Exemple d'enregistrement (à adapter à ton modèle)
                EcritureJournal.objects.create(
                    date=date if date else None,
                    compte=compte,
                    nom=nom,
                    libelle=libelle,
                    quantite=quantite or 0,
                    taux=taux or 0,
                    debit=debit or 0,
                    credit=credit or 0,
                    journal=journal
                )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
