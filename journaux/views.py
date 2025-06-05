from django.shortcuts import render




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
