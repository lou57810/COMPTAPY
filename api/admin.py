from django.contrib import admin
from .models import Journal, CompteComptable, EcritureJournal, Entreprise

# Register your models here.
admin.site.register(Journal)
admin.site.register(CompteComptable)
admin.site.register(EcritureJournal)
# admin.site.register(Entreprise)

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ("nom", "siret", "ape", "owner")
    search_fields = ("nom", "siret")
    list_filter = ("ape",)
