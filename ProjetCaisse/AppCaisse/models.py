from django.db import models
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


class Facture(models.Model):
    
    nom_patient = models.CharField(max_length=100)
    prenom_patient = models.CharField(max_length=100)
    caisse = models.CharField(max_length=100)
    date = models.DateField()
    reduction = models.DecimalField(max_digits=10, decimal_places=2)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montant_remis = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    examen = models.CharField(max_length=100)
    encaisse = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mode_paiement = models.CharField(max_length=100, default="Cash") 

    def __str__(self):
        return f"Facture de {self.nom_patient} {self.prenom_patient}"


from django.db import models
from AppCaisse.models import Facture

class Dette(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    examen = models.CharField(max_length=100)
    date = models.DateField()
    caisse = models.CharField(max_length=100)    

    def __str__(self):
        return f"Dette de {self.nom} {self.prenom}"

class Comptabilite(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    examen = models.CharField(max_length=100)
    date = models.DateField()
    caisse = models.CharField(max_length=100)

from django.db import models

class RetraitCaisse(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    caisse = models.CharField(max_length=100, default='Secretariat')
    date = models.DateTimeField(auto_now_add=True)
    motif = models.TextField()

    def __str__(self):
        return f"Retrait de {self.montant} le {self.date}"
    
from django.db import models

class ResultatCalcul(models.Model):
    jour = models.DateField()
    caisse = models.CharField(max_length=100)
    somme_disponible = models.DecimalField(max_digits=10, decimal_places=2)
  

    



