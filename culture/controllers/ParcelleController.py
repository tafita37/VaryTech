# views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from culture.model.Parcelle import Parcelle
from culture.model.TypeSol import TypeSol
from django.core.files.storage import FileSystemStorage

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

@require_POST
def new_parcelle(request):
    print("yo")
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