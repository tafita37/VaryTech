# views.py
from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
import requests
from culture.model.AlerteCulture import AlerteCulture
from culture.model.AlerteRecolte import AlerteRecolte
from culture.model.Culture import Culture
from culture.model.CultureRessource import CultureRessource
from culture.model.Parcelle import Parcelle
from culture.model.Produit import Produit
from culture.model.Recolte import Recolte
from culture.model.Ressource import Ressource
from culture.model.TypeSol import TypeSol
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.contrib import messages
from django.db.models import Sum

import uuid
import os

API_KEY = "bd6e5a5b4a934bb8b9c90042251511"   # Mets ta vraie clé ici
BASE_URL = "https://api.weatherapi.com/v1/future.json"  # Exemple WeatherAPI

@require_GET
def parcelle_list_page(request):
    parcelles=Parcelle.objects.all()
    typeSols=TypeSol.objects.all()
    context = {
        # "css_css" : ['vertical-layout-light/style.css'],
        "parcelles" : parcelles,
        "MEDIA_URL": settings.MEDIA_URL,
        "titre_inner" : "Parcelles",
        "typeSols" : typeSols
    }
    return render(request, "views/parcelle_list.html", context)

@require_GET
def culture_list_page(request, parcelle_id):
    parcelle=Parcelle.objects.get(id=parcelle_id)
    cultures=Culture.objects.filter(parcelle=parcelle_id)
    ressources=Ressource.objects.all()
    produits=Produit.objects.all()
    context = {
        # "css_css" : ['vertical-layout-light/style.css'],
        "cultures" : cultures,
        "parcelle" : parcelle,
        "produits" : produits,
        "ressources" : ressources,
        "MEDIA_URL": settings.MEDIA_URL,
        "titre_inner" : "Cultures",
    }
    return render(request, "views/culture_list.html", context)

@require_GET
def culture_detail_page(request, culture_id):
    culture=Culture.objects.get(id=culture_id)
    culturesRessources=CultureRessource.objects.filter(culture=culture_id)
    recoltes=Recolte.objects.filter(culture=culture_id)
    context = {
        # "css_css" : ['vertical-layout-light/style.css'],
        "culture" : culture,
        "recoltes" : recoltes,
        "culturesRessources" : culturesRessources,
        "MEDIA_URL": settings.MEDIA_URL,
        "titre_inner" : "Culture de "+culture.produit.nom,
    }
    return render(request, "views/culture_detail.html", context)

@require_POST
def new_parcelle(request):
    nom = request.POST.get('nom')
    superficie = request.POST.get('superficie')
    humiditeMoyenne = request.POST.get('humiditeMoyenne')
    temperatureMoyenne = request.POST.get('temperatureMoyenne')
    typeSol = request.POST.get('typeSol')
    photo = request.FILES.get('photo')
    oldname=photo.name if photo else None
    if photo:
        ext = os.path.splitext(photo.name)[1]
        new_filename = f"{uuid.uuid4()}{ext}"
        photo.name = new_filename
        fs = FileSystemStorage()
        filename = fs.save(new_filename, photo)
        uploaded_file_url = fs.url(filename)
        print(f"Fichier renommé et sauvegardé à : {uploaded_file_url}")
    parcelle=Parcelle(
        nom=nom,
        superficie=superficie,
        humiditeMoyenne=humiditeMoyenne,
        temperatureMoyenne=temperatureMoyenne,
        sol=TypeSol.objects.get(id=typeSol),
        photoA=oldname,
        photoE=new_filename
    )
    parcelle.save()
    return redirect('parcelle_page')

@require_POST
def new_culture(request):
    produit_id = request.POST.get('produit')
    parcelle_id = request.POST.get('parcelle')

    try:
        produit = Produit.objects.get(id=produit_id)
        alerteCulture = AlerteCulture.objects.get(produit=produit)
    except Produit.DoesNotExist:
        messages.error(request, "Produit introuvable")
        return redirect('culture_page', parcelle_id=parcelle_id)
    except AlerteCulture.DoesNotExist:
        messages.error(request, "Alerte météo pour ce produit non définie")
        return redirect('culture_page', parcelle_id=parcelle_id)

    dateSemis = request.POST.get('dateSemis')
    if datetime.strptime(dateSemis, "%Y-%m-%d").date() >= datetime.today().date() + timedelta(days=14):
        # --- Vérification météo ---
        city = "Antananarivo"
        days = 1  # Prévision du jour courant
        conditions_ok = False

        try:
            response = requests.get(
                BASE_URL,
                params={"key": API_KEY, "q": city, "dt": dateSemis},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            forecast = data['forecast']['forecastday'][0]['day']

            temp_ok = alerteCulture.temperatureMin <= forecast['avgtemp_c'] <= alerteCulture.temperatureMax
            humid_ok = alerteCulture.humiditeMin <= forecast.get('avghumidity', 0) <= alerteCulture.humiditeMax
            vent_ok = forecast.get('maxwind_kph', 0) <= alerteCulture.vitesseVent

            conditions_ok = temp_ok and humid_ok and vent_ok
        except Exception as e:
            messages.warning(request, f"Impossible de récupérer la météo : {e}")

        if not conditions_ok:
            messages.warning(request, "Les conditions météo ne sont pas favorables pour cette culture")

    # --- Récupération des autres données ---
    dateRecoltePrevue = request.POST.get('dateRecoltePrevue')
    rendementEstime = request.POST.get('rendementEstime')
    quantiteSemee = request.POST.get('quantiteSemee')
    photo = request.FILES.get('photo')
    ressources = request.POST.getlist('ressource[]')
    quantites = request.POST.getlist('quantite[]')
    temperatureMin = request.POST.get('temperatureMin')
    temperatureMax = request.POST.get('temperatureMax')
    humiditeMin = request.POST.get('humiditeMin')
    humiditeMax = request.POST.get('humiditeMax')
    vitesseVent = request.POST.get('vitesseVent')
    oldname = photo.name if photo else None
    new_filename = None

    if photo:
        ext = os.path.splitext(photo.name)[1]
        new_filename = f"{uuid.uuid4()}{ext}"
        photo.name = new_filename
        fs = FileSystemStorage()
        fs.save(new_filename, photo)

    if not ressources:
        ressources = request.POST.getlist('ressource')
    if not quantites:
        quantites = request.POST.getlist('quantite')

    if len(ressources) != len(quantites):
        messages.error(request, "Quantité ou ressource non entré")
        return redirect('culture_page', parcelle_id=parcelle_id)

    # --- Création de la culture et des ressources liées ---
    with transaction.atomic():
        culture = Culture.objects.create(
            produit=produit,
            parcelle=Parcelle.objects.get(id=parcelle_id),
            dateSemis=dateSemis,
            dateRecoltePrevu=dateRecoltePrevue,
            rendementEstime=rendementEstime,
            quantiteSemee=quantiteSemee,
            photoA=oldname,
            photoE=new_filename
        )
        alerte=AlerteRecolte(
            culture=culture,
            temperatureMin=temperatureMin,
            temperatureMax=temperatureMax, 
            humiditeMin=humiditeMin,
            humiditeMax=humiditeMax,
            vitesseVent=vitesseVent
        )
        alerte.save()

        for r_id, q in zip(ressources, quantites):
            if not r_id or not q:
                continue
            try:
                q_val = float(q)
            except (ValueError, TypeError):
                continue
            CultureRessource.objects.create(
                culture=culture,
                ressource=Ressource.objects.get(id=r_id),
                quantiteResource=q_val
            )

    return redirect('culture_page', parcelle_id=parcelle_id)

@require_POST
def new_recolte(request):
    dateRecolte = request.POST.get('dateRecolte')
    culture = Culture.objects.get(id=request.POST.get('culture'))
    alerteRecolte= AlerteRecolte.objects.get(culture=Culture.objects.get(id=request.POST.get('culture')))
    if datetime.strptime(dateRecolte, "%Y-%m-%d").date() >= datetime.today().date() + timedelta(days=14):
        # --- Vérification météo ---
        city = "Antananarivo"
        days = 1  # Prévision du jour courant
        conditions_ok = False

        try:
            response = requests.get(
                BASE_URL,
                params={"key": API_KEY, "q": city, "dt": dateRecolte},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            forecast = data['forecast']['forecastday'][0]['day']

            temp_ok = alerteRecolte.temperatureMin <= forecast['avgtemp_c'] <= alerteRecolte.temperatureMax
            humid_ok = alerteRecolte.humiditeMin <= forecast.get('avghumidity', 0) <= alerteRecolte.humiditeMax
            vent_ok = forecast.get('maxwind_kph', 0) <= alerteRecolte.vitesseVent

            conditions_ok = temp_ok and humid_ok and vent_ok
        except Exception as e:
            messages.warning(request, f"Impossible de récupérer la météo : {e}")

        if not conditions_ok:
            messages.warning(request, "Les conditions météo ne sont pas favorables pour cette récolte")
    quantiteRecoltee = float(request.POST.get('quantiteRecoltee'))
    total_recolte = float(Recolte.objects.filter(culture=culture).aggregate(total=Sum('quantiteRecoltee'))['total'] or 0)
    total_recolte += float(quantiteRecoltee)
    culture.rendementReel=float(culture.quantiteSemee)/float(total_recolte)
    culture.save()
    recolte=Recolte(
        culture=culture,
        dateRecolte=dateRecolte,
        quantiteRecoltee=quantiteRecoltee
    )
    recolte.save()
    return redirect('culture_detail_page', culture_id=culture.id)