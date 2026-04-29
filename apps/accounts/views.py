# ─── apps/accounts/views.py ───────────────────────────────────────────────────
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ProfilForm, ChangerMotDePasseForm
from .models import User


def inscription(request):
    """Inscription d'un nouvel utilisateur."""
    if request.user.is_authenticated:
        return redirect('pronostics:home')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} ! Votre compte a été créé.")
            return redirect('pronostics:home')
    else:
        form = InscriptionForm()

    return render(request, 'accounts/inscription.html', {'form': form})


def connexion(request):
    """Connexion utilisateur."""
    if request.user.is_authenticated:
        return redirect('pronostics:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'pronostics:home')
            return redirect(next_url)
        else:
            messages.error(request, "Email ou mot de passe incorrect.")

    return render(request, 'accounts/connexion.html')


@login_required
def deconnexion(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('pronostics:home')


@login_required
def profil(request):
    """Page de profil et modification des infos personnelles."""
    user = request.user

    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('accounts:profil')
    else:
        form = ProfilForm(instance=user)

    return render(request, 'accounts/profil.html', {'form': form})


@login_required
def changer_mot_de_passe(request):
    if request.method == 'POST':
        form = ChangerMotDePasseForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Mot de passe modifié avec succès.")
            return redirect('accounts:profil')
    else:
        form = ChangerMotDePasseForm(request.user)
    return render(request, 'accounts/changer_mdp.html', {'form': form})
