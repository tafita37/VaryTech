# views.py
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from authentification.model.Admin import Admin
from authentification.model.Role import Role
from authentification.model.Utilisateur import Utilisateur
from django.contrib import messages
from django.contrib.auth import logout

@require_GET
def register_user_page(request):
    roles=Role.objects.all()
    context = {
        # "css_css" : ['vertical-layout-light/style.css'],
        "titre_inner" : "Mon Compte",
        "roles" : roles
    }
    return render(request, "views/register_user.html", context)

@require_GET
def login_user_page(request):
    context = {
        # "css_css" : ['vertical-layout-light/style.css'],
        "titre_inner" : "Mon Compte",
    }
    return render(request, "views/login_user.html", context)

@require_POST
def register_user(request):
    nom = request.POST.get('nom')
    prenom = request.POST.get('prenom')
    username = request.POST.get('username')
    role = request.POST.get('role')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    if password != confirm_password:
        raise Exception("Le mot de passe ne correspond pas.")
    user=Utilisateur(
        nom=nom,
        prenom=prenom,
        username=username,
        role=Role.objects.get(id=role),
        password=password
    )
    user.save()
    request.session['user_id'] = user.id
    return redirect('register_user_page')

@require_POST
def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user = Admin.objects.get(username=username, password=password)
        request.session['user_id'] = user.id
        return redirect('parcelle_page')  # page après connexion réussie
    except Utilisateur.DoesNotExist:
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
        return redirect('home')
    
@require_GET
def logout_url(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login_user_page')