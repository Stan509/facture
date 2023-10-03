from django import forms
from .models import Facture, Dette, Comptabilite
from django.core import validators

    

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['nom_patient', 'prenom_patient', 'caisse', 'date', 'reduction', 'montant_paye', 'examen', 'prix', 'total', 'balance', 'montant_remis', 'encaisse']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['examen'].widget.attrs.update({'id': 'id_examen'})
        self.fields['prix'].widget = forms.HiddenInput()  # Champs caché pour le prix
        self.fields['total'].widget = forms.HiddenInput()  # Champs caché pour le total
        self.fields['balance'].widget = forms.HiddenInput()  # Champs caché pour la balance
        self.fields['montant_remis'].widget = forms.HiddenInput()  # Champs caché pour le montant remis



class DetteForm(forms.ModelForm):
    class Meta:
        model = Dette
        fields = ['nom', 'prenom', 'montant', 'examen', 'date', 'caisse']

    def __init__(self, *args, **kwargs):
        super(DetteForm, self).__init__(*args, **kwargs)
    
class ComptabiliteForm(forms.ModelForm):
    class Meta:
        model = Comptabilite
        fields = ['nom', 'prenom', 'montant', 'examen', 'date', 'caisse']

    def __init__(self, *args, **kwargs):
        super(ComptabiliteForm, self).__init__(*args, **kwargs)


from django import forms
from .models import RetraitCaisse

class RetraitCaisseForm(forms.ModelForm):
    class Meta:
        model = RetraitCaisse
        fields = ['montant', 'motif', 'caisse']
