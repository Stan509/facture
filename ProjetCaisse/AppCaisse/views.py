from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date

# Create your views here.
from django.shortcuts import render

def acceuil(request):
    factures = Facture.objects.all()
    context = {'factures': factures}
    return render(request, 'acceuil.html', context)

    



from django.shortcuts import render, redirect
from .models import Comptabilite, Facture
from .forms import FactureForm
from django.shortcuts import render, redirect
from django.template import RequestContext

from django.shortcuts import render, redirect
from .models import Facture
from .forms import FactureForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Dette
from .forms import FactureForm  # Assurez-vous d'importer le formulaire Facture approprié

def enregistrer_facture(request):
    if request.method == 'POST':
        # Créez une instance du formulaire avec les données soumises
        form = FactureForm(request.POST)

        if form.is_valid():
            # Le formulaire est valide, enregistrez les données dans la base de données
            facture = form.save()

            # Si la balance de la facture est supérieure à zéro, créez une dette
            if facture.balance > 0:
                nouvelle_dette = Dette(
                    facture=facture,
                    nom=facture.nom_patient,
                    prenom=facture.prenom_patient,
                    examen=facture.examen,
                    date=facture.date,
                    caisse=facture.caisse,
                    montant=facture.balance
                )
                nouvelle_dette.save()

            if facture.encaisse > 0:
                nouvelle_comptabilite = Comptabilite(
                    facture=facture,
                    nom=facture.nom_patient,
                    prenom=facture.prenom_patient,
                    examen=facture.examen,
                    date=facture.date,
                    caisse=facture.caisse,
                    montant=facture.encaisse
                )
                nouvelle_comptabilite.save()

            # Retournez une réponse appropriée, par exemple, une redirection vers la page précédente
            return HttpResponseRedirect(reverse('acceuil'))

    else:
        # Si la méthode de la requête est GET, affichez simplement le formulaire
        form = FactureForm()

    context = {'form': form}
    return render(request, 'acceuil.html', context)

    # Reste du code pour le traitement du formulaire



 # Assurez-vous d'importer votre modèle Facture


from django.http import FileResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
from io import BytesIO
from django.views import View
from .models import Facture

class FacturePDFView(View):
    def get(self, request, facture_id):
        # Récupérez la facture depuis la base de données
        facture = get_object_or_404(Facture, id=facture_id)

        # Chargez le modèle HTML pour le PDF
        template = get_template('facture_template.html')
        context = {'facture': facture}

        # Remplissez le modèle HTML avec les données de la facture
        html = template.render(context)

        # Créez un objet PDF
        pdf = BytesIO()
        pisa.CreatePDF(BytesIO(html.encode('UTF-8')), pdf)

        # Renvoyez le PDF en tant que réponse
        pdf.seek(0)
        response = FileResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="facture_{facture.id}.pdf"'
        return response

from django.shortcuts import render
from .models import Dette  # Assurez-vous que vous importez correctement votre modèle Dette

def liste_dette(request):
    # Récupérez toutes les dettes depuis la base de données
    dettes = Dette.objects.all()
    
    # Passez les dettes au modèle
    return render(request, 'dette.html', {'dettes': dettes})

from django.shortcuts import render, redirect
from .models import Dette
from .forms import DetteForm
from .models import Dette
from .forms import DetteForm

def liste_et_ajout_dette(request):
    if request.method == 'POST':
        form = DetteForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigez l'utilisateur vers une page de confirmation ou une autre vue
            return redirect('nom_de_la_vue')
    else:
        form = DetteForm()

    # Récupérez toutes les dettes depuis la base de données pour les afficher dans la liste
    dettes = Dette.objects.all()

    context = {'form': form, 'dettes': dettes}
    return render(request, 'dette.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Dette
from .forms import DetteForm  # Assurez-vous d'importer le formulaire de dette approprié

# Vue pour afficher la liste des dettes
def liste_dettes(request):
    dettes = Dette.objects.all()
    return render(request, 'dette.html', {'dettes': dettes})

# Vue pour ajouter une dette
def ajouter_dette(request):
    if request.method == 'POST':
        form = DetteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_dettes')
    else:
        form = DetteForm()
    return render(request, 'ajouter_dette.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Dette
from .forms import DetteForm  # Assurez-vous d'importer le formulaire approprié

def modifier_dette(request, dette_id):
    # Récupérer la dette à modifier depuis la base de données
    dette = get_object_or_404(Dette, pk=dette_id)

    if request.method == 'POST':
        # Si la requête est POST, cela signifie que le formulaire de modification a été soumis
        form = DetteForm(request.POST, instance=dette)  # Utilisez le formulaire avec l'instance de la dette existante

        if form.is_valid():
            # Le formulaire est valide, enregistrez les modifications
            form.save()
            return redirect('liste_et_ajout_dette')  # Redirigez vers la liste des dettes

    else:
        # Si la requête est GET, affichez le formulaire rempli avec les données actuelles de la dette
        form = DetteForm(instance=dette)

    return render(request, 'modifier_dette.html', {'form': form, 'dette': dette})

# Vue pour supprimer une dette
def supprimer_dette(request, dette_id):
    dette = get_object_or_404(Dette, pk=dette_id)

    if request.method == 'POST':
        # Créez une nouvelle entrée de comptabilité en utilisant les données de la dette
        Comptabilite.objects.create(
            facture=dette.facture,
            nom=dette.nom,
            prenom=dette.prenom,
            montant=dette.montant,
            examen=dette.examen,
            date=timezone.now(),
            caisse=dette.caisse,
        )

        # Supprimez la dette existante
        dette.delete()

        return redirect('liste_et_ajout_dette')

    return render(request, 'dette.html', {'dette': dette}) # Redirigez vers la liste des dettes après suppression


from django.shortcuts import render, redirect
from .models import RetraitCaisse
from .forms import RetraitCaisseForm  # Assurez-vous d'avoir un formulaire de retrait

def page_retraits(request):
    retraits = RetraitCaisse.objects.all()
    form = RetraitCaisseForm()  # Remplacez-le par le nom de votre formulaire de retrait

    if request.method == 'POST':
        form = RetraitCaisseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('page_retraits')  # Redirigez vers la même page après l'ajout

    context = {'retraits': retraits, 'form': form}
    return render(request, 'retrait.html', context)

from django.http import JsonResponse
from .models import Comptabilite, ResultatCalcul
from django.db.models import Sum
from django.shortcuts import render
from django.utils.dateparse import parse_date
import json
# Dans views.py
from django.http import JsonResponse
from .models import Comptabilite
from django.db.models import Sum
from datetime import datetime  # Importez datetime

def calcul_somme_disponible(request):
    if request.method == 'POST':
        action = request.POST.getlist('action')

        if 'Calculer' in action:
            caisse_selectionnee = request.POST.get('caisse')
            date_selectionnee = request.POST.get('date')

            # Formatez la date correctement en utilisant datetime
            date_obj = datetime.strptime(date_selectionnee, '%b. %d, %Y').strftime('%Y-%m-%d')

            resultats = Comptabilite.objects.filter(
                caisse=caisse_selectionnee,
                date=date_obj
            ).values('date', 'caisse').annotate(
                somme_disponible=Sum('montant')
            )

            resultats_liste = list(resultats)

            # Enregistrez les résultats dans le modèle ResultatCalcul
            for resultat in resultats_liste:
                jour = resultat['date']
                caisse = resultat['caisse']
                somme_disponible = resultat['somme_disponible']

                # Créez une instance ResultatCalcul et enregistrez-la
                resultat_calcul, created = ResultatCalcul.objects.get_or_create(jour=jour, caisse=caisse)
                resultat_calcul.somme_disponible = somme_disponible
                resultat_calcul.save()

            return JsonResponse(resultats_liste, safe=False)

        elif 'Enregistrer' in action:
            # Vous pouvez implémenter le code pour enregistrer le résultat ici
            pass

    return JsonResponse([], safe=False)

def votre_vue_de_comptabilite(request):
    # Récupérez toutes les caisses distinctes depuis la base de données Comptabilite
    caisses_disponibles = Comptabilite.objects.values('caisse').distinct()

    # Récupérez toutes les dates distinctes depuis la base de données Comptabilite
    dates_disponibles = Comptabilite.objects.values('date').distinct().order_by('-date')

    # Si un formulaire est soumis, effectuez le calcul et enregistrez le résultat
    somme_disponible = None
    if request.method == 'POST':
        caisse = request.POST.get('caisse', None)
        date = request.POST.get('date', None)

        # Effectuez le calcul de la somme disponible pour la caisse et la date sélectionnées
        if caisse and date:
            date_obj = parse_date(date)  # Convertissez la date en objet Date
            somme_disponible = Comptabilite.objects.filter(caisse=caisse, date=date_obj).aggregate(somme_disponible=Sum('montant'))['somme_disponible']
       
        if 'enregistrer' in request.POST:
            # Enregistrez le résultat dans le modèle ResultatCalcul
            resultat, created = ResultatCalcul.objects.get_or_create(jour=date_obj, caisse=caisse)
            resultat.somme_disponible = somme_disponible
            resultat.save()

    # Récupérez les résultats stockés dans le modèle ResultatCalcul pour affichage
    resultats = ResultatCalcul.objects.all()

    # Passez les caisses, les dates, la somme disponible et les résultats à votre modèle HTML
    context = {
        'caisses_disponibles': caisses_disponibles,
        'dates_disponibles': dates_disponibles,
        'somme_disponible': somme_disponible,
        'resultats': resultats,
    }

    return render(request, 'comptabilite.html', context)


from django.shortcuts import render
from .models import Comptabilite, ResultatCalcul
from django.db.models import Sum
from django.utils.dateparse import parse_date

def calcul_et_enregistrement(request):
    if request.method == 'POST':
        caisse = request.POST.get('caisse', None)
        date = request.POST.get('date', None)

        # Effectuez le calcul de la somme disponible pour la caisse et la date sélectionnées
        if caisse and date:
            date_obj = parse_date(date)  # Convertissez la date en objet Date
            somme_disponible = Comptabilite.objects.filter(caisse=caisse, date=date_obj).aggregate(somme_disponible=Sum('montant'))['somme_disponible']

            # Enregistrez le résultat dans le modèle ResultatCalcul
            resultat, created = ResultatCalcul.objects.get_or_create(jour=date_obj, caisse=caisse)
            resultat.somme_disponible = somme_disponible
            resultat.save()

    # Redirigez l'utilisateur vers une autre page ou affichez un message de confirmation ici
            return render(request, 'comptabilite.html')
