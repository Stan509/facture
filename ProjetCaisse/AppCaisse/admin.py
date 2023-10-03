from django.db.models import Sum
from django.contrib import admin
from .models import Facture, Dette, Comptabilite, ResultatCalcul


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_patient', 'prenom_patient', 'caisse', 'date', 'reduction', 'montant_paye', 'balance', 'montant_remis', 'prix', 'total', 'encaisse')
    list_filter = ('caisse', 'date')
    search_fields = ('nom_patient', 'prenom_patient', 'date', 'id')
    def total_caisse_par_jour(self, obj):
        # Utilisez l'agrégation Sum pour additionner les valeurs de la caisse par jour
        total_caisse = Facture.objects.filter(date=obj.date).aggregate(Sum('caisse'))['caisse__sum']
        return total_caisse or 0.0

    total_caisse_par_jour.short_description = 'Total de la caisse par jour'
    

    # Vous pouvez ajouter d'autres options de configuration ici

# Enregistrez votre modèle Facture avec la classe d'administration FactureAdmin



@admin.register(Dette)
class DetteAdmin(admin.ModelAdmin):
    list_display = ('facture', 'nom', 'prenom', 'montant', 'examen', 'date', 'caisse')
    list_filter = ('nom', 'prenom')
    search_fields = ('nom', 'prenom')
    # Autres options de configuration



@admin.register(Comptabilite)
class ComptabiliteAdmin(admin.ModelAdmin):
    list_display = ('facture', 'nom', 'prenom', 'montant', 'examen', 'date', 'caisse')
    list_filter = ('date', 'caisse')
    search_fields = ('date', 'caisse')

from django.contrib import admin
from .models import RetraitCaisse

@admin.register(RetraitCaisse)
class RetraitCaisseAdmin(admin.ModelAdmin):
    list_display = ('id', 'montant', 'date', 'caisse', 'motif')

@admin.register(ResultatCalcul)
class ResultatCalculAdmin(admin.ModelAdmin):
    list_display = ('jour', 'caisse', 'somme_disponible')
    list_filter = ('jour', 'caisse')
    search_fields = ('jour__isoformat', 'caisse')