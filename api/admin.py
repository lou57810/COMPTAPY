from django.contrib import admin
from .models import Journal, CompteComptable, EcritureJournal

# Register your models here.
admin.site.register(Journal)
admin.site.register(CompteComptable)
admin.site.register(EcritureJournal)
