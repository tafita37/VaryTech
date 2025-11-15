# views.py
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_GET, require_POST
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
    produit = request.POST.get('produit')
    parcelle = request.POST.get('parcelle')
    dateSemis = request.POST.get('dateSemis')
    dateRecoltePrevue = request.POST.get('dateRecoltePrevue')
    rendementEstime = request.POST.get('rendementEstime')
    quantiteSemee = request.POST.get('quantiteSemee')
    photo = request.FILES.get('photo')
    ressources = request.POST.getlist('ressource[]')
    quantites = request.POST.getlist('quantite[]')
    oldname=photo.name if photo else None
    if photo:
        ext = os.path.splitext(photo.name)[1]
        new_filename = f"{uuid.uuid4()}{ext}"
        photo.name = new_filename
        fs = FileSystemStorage()
        filename = fs.save(new_filename, photo)
        uploaded_file_url = fs.url(filename)
        print(f"Fichier renommé et sauvegardé à : {uploaded_file_url}")
     # fallback: si ton navigateur envoie sans crochets, tester aussi
    if not ressources:
        ressources = request.POST.getlist('ressource')
    if not quantites:
        quantites = request.POST.getlist('quantite')

    # validation minimale : mêmes longueurs
    if len(ressources) != len(quantites):
        messages.error(request, "Quantité ou ressource non entré")
        return redirect('culture_page', parcelle_id=parcelle)

    with transaction.atomic():
        # création de la culture
        culture = Culture.objects.create(
            produit=Produit.objects.get(id=produit),
            parcelle=Parcelle.objects.get(id=parcelle),
            dateSemis=dateSemis,
            dateRecoltePrevu=dateRecoltePrevue,
            rendementEstime=rendementEstime,
            quantiteSemee=quantiteSemee,
            statut=0,
            photoA=oldname,
            photoE=new_filename
        )

        # enregistrement des ressources liées
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
    return redirect('culture_page', parcelle_id=parcelle)

@require_POST
def new_recolte(request):
    dateRecolte = request.POST.get('dateRecolte')
    quantiteRecoltee = float(request.POST.get('quantiteRecoltee'))
    culture = Culture.objects.get(id=request.POST.get('culture'))
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