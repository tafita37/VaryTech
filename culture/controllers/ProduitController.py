# views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from culture.model.AlerteCulture import AlerteCulture
from culture.model.Produit import Produit

@require_GET
def produit_list_page(request):
    produits=Produit.objects.all()
    context = {
        # "css_css" : ['vertical-layout-light/style.css'],
        "produits" : produits,
        "MEDIA_URL": settings.MEDIA_URL,
        "titre_inner" : "Produit",
    }
    return render(request, "views/produit_list.html", context)

@require_GET
def modif_alerte_meteo_produit_page(request, produit_id):
    produit=Produit.objects.get(id=produit_id)
    alerteCulture=AlerteCulture.objects.get(produit=produit)
    context = {
        # "css_css" : ['vertical-layout-light/style.css'],
        "produit" : produit,
        "alerteCulture" : alerteCulture,
        "MEDIA_URL": settings.MEDIA_URL,
        "titre_inner" : "Alerte Météo",
    }
    return render(request, "views/modif_alerte_meteo_produit.html", context)

@require_POST
def new_produit(request):
    nom = request.POST.get('nom')
    prixUnitaire = request.POST.get('prixUnitaire')
    temperatureMin = request.POST.get('temperatureMin')
    temperatureMax = request.POST.get('temperatureMax')
    humiditeMin = request.POST.get('humiditeMin')
    humiditeMax = request.POST.get('humiditeMax')
    vitesseVent = request.POST.get('vitesseVent')
    produit=Produit(
        nom=nom,
        prix=prixUnitaire
    )
    produit.save()
    alerte=AlerteCulture(
        produit=produit,
        temperatureMin=temperatureMin,
        temperatureMax=temperatureMax, 
        humiditeMin=humiditeMin,
        humiditeMax=humiditeMax,
        vitesseVent=vitesseVent
    )
    alerte.save()
    return redirect('produit_page')

@require_POST
def modif_alerte_culture(request):
    temperatureMin = request.POST.get('temperatureMin')
    temperatureMax = request.POST.get('temperatureMax')
    humiditeMin = request.POST.get('humiditeMin')
    humiditeMax = request.POST.get('humiditeMax')
    vitesseVent = request.POST.get('vitesseVent')
    produit=request.POST.get('produit_id')
    alerte=AlerteCulture(
        produit=Produit.objects.get(id=produit),
        temperatureMin=temperatureMin,
        temperatureMax=temperatureMax, 
        humiditeMin=humiditeMin,
        humiditeMax=humiditeMax,
        vitesseVent=vitesseVent
    )
    alerte.save()
    return redirect('produit_page')