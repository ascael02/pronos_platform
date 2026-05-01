"""
Vues pour la gestion des pronostics.
CRUD complet avec contrôle d'accès VIP.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import Pronostic, Match, Sport, Competition, CommentairePronostic
from .forms import PronosticForm, CommentaireForm, MatchForm
from apps.bookmakers.models import Bookmaker


def home(request):
    """Page d'accueil avec les derniers pronostics et statistiques."""
    pronostics_recents = Pronostic.objects.filter(
        publie=True, est_vip=False
    ).select_related('match', 'match__competition', 'auteur', 'bookmaker')[:6]

    pronostics_vip = Pronostic.objects.filter(
        publie=True, est_vip=True
    ).select_related('match', 'auteur')[:3]

    # Stats globales
    total = Pronostic.objects.filter(publie=True).exclude(resultat='pending')
    wins = total.filter(resultat='win').count()
    total_count = total.count()
    taux_reussite = round((wins / total_count * 100), 1) if total_count > 0 else 0

    # Top bookmakers
    bookmakers = Bookmaker.objects.filter(actif=True).order_by('ordre')[:4]

    # Sports actifs
    sports = Sport.objects.filter(actif=True)

    ctx = {
        'pronostics_recents': pronostics_recents,
        'pronostics_vip': pronostics_vip,
        'taux_reussite': taux_reussite,
        'total_pronostics': total_count,
        'total_wins': wins,
        'bookmakers': bookmakers,
        'sports': sports,
    }
    return render(request, 'home.html', ctx)


def liste_pronostics(request):
    """Liste paginée de tous les pronostics avec filtres."""
    qs = Pronostic.objects.filter(publie=True).select_related(
        'match', 'match__competition', 'match__competition__sport', 'auteur', 'bookmaker'
    )

    # Filtres
    sport_slug = request.GET.get('sport')
    resultat = request.GET.get('resultat')
    vip_only = request.GET.get('vip')
    search = request.GET.get('q')

    if sport_slug:
        qs = qs.filter(match__competition__sport__slug=sport_slug)
    if resultat and resultat in ('win', 'loss', 'pending'):
        qs = qs.filter(resultat=resultat)
    if vip_only:
        qs = qs.filter(est_vip=True)
    if search:
        qs = qs.filter(
            Q(titre__icontains=search) |
            Q(match__equipe_domicile__icontains=search) |
            Q(match__equipe_exterieur__icontains=search)
        )

    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))

    ctx = {
        'page_obj': page,
        'sports': Sport.objects.filter(actif=True),
        'sport_actif': sport_slug,
        'resultat_actif': resultat,
        'search': search,
    }
    return render(request, 'pronostics/liste.html', ctx)


def detail_pronostic(request, slug):
    """Détail d'un pronostic. Contenu VIP masqué pour non-abonnés."""
    prono = get_object_or_404(Pronostic, slug=slug, publie=True)

    # Contrôle d'accès VIP
    peut_voir_analyse = True
    if prono.est_vip:
        if not request.user.is_authenticated or not request.user.is_vip:
            peut_voir_analyse = False

    # Incrémenter les vues
    Pronostic.objects.filter(pk=prono.pk).update(vues=prono.vues + 1)

    # Commentaires
    commentaires = prono.commentaires.filter(approuve=True).select_related('auteur')
    form_commentaire = CommentaireForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form_commentaire = CommentaireForm(request.POST)
        if form_commentaire.is_valid():
            c = form_commentaire.save(commit=False)
            c.pronostic = prono
            c.auteur = request.user
            c.save()
            messages.success(request, "Commentaire ajouté avec succès.")
            return redirect('pronostics:detail', slug=slug)

    # Pronostics similaires
    similaires = Pronostic.objects.filter(
        match__competition=prono.match.competition, publie=True
    ).exclude(pk=prono.pk)[:4]

    ctx = {
        'prono': prono,
        'peut_voir_analyse': peut_voir_analyse,
        'commentaires': commentaires,
        'form_commentaire': form_commentaire,
        'similaires': similaires,
    }
    return render(request, 'pronostics/detail.html', ctx)


@login_required
@staff_member_required
def creer_pronostic(request):
    """Création d'un nouveau pronostic (staff uniquement)."""
    if request.method == 'POST':
        form = PronosticForm(request.POST)
        if form.is_valid():
            prono = form.save(commit=False)
            prono.auteur = request.user
            prono.save()
            messages.success(request, f"Pronostic « {prono.titre} » créé avec succès.")
            return redirect('pronostics:detail', slug=prono.slug)
    else:
        form = PronosticForm()

    return render(request, 'pronostics/form.html', {'form': form, 'action': 'Créer'})


@login_required
@staff_member_required
def modifier_pronostic(request, slug):
    """Modification d'un pronostic existant."""
    prono = get_object_or_404(Pronostic, slug=slug)

    if request.method == 'POST':
        form = PronosticForm(request.POST, instance=prono)
        if form.is_valid():
            form.save()
            messages.success(request, "Pronostic mis à jour avec succès.")
            return redirect('pronostics:detail', slug=prono.slug)
    else:
        form = PronosticForm(instance=prono)

    return render(request, 'pronostics/form.html', {'form': form, 'action': 'Modifier', 'prono': prono})


@login_required
@staff_member_required
def supprimer_pronostic(request, slug):
    """Suppression d'un pronostic avec confirmation."""
    prono = get_object_or_404(Pronostic, slug=slug)

    if request.method == 'POST':
        titre = prono.titre
        prono.delete()
        messages.success(request, f"Pronostic « {titre} » supprimé.")
        return redirect('pronostics:liste')

    return render(request, 'pronostics/confirmer_suppression.html', {'prono': prono})


def statistiques(request):
    """Tableau de statistiques globales et par sport."""
    from django.db.models import Case, When, IntegerField, Sum

    pronostics = Pronostic.objects.filter(publie=True).exclude(resultat='pending')

    # Stats globales
    total = pronostics.count()
    wins = pronostics.filter(resultat='win').count()
    losses = pronostics.filter(resultat='loss').count()
    voids = pronostics.filter(resultat='void').count()
    taux = round((wins / total * 100), 1) if total > 0 else 0

    # Stats par sport
    stats_sports = []
    for sport in Sport.objects.filter(actif=True):
        qs = pronostics.filter(match__competition__sport=sport)
        t = qs.count()
        w = qs.filter(resultat='win').count()
        stats_sports.append({
            'sport': sport,
            'total': t,
            'wins': w,
            'losses': qs.filter(resultat='loss').count(),
            'taux': round((w / t * 100), 1) if t > 0 else 0,
        })

    # Historique mensuel (12 derniers mois)
    from django.db.models.functions import TruncMonth
    historique = pronostics.annotate(
        mois=TruncMonth('created_at')
    ).values('mois').annotate(
        total=Count('id'),
        wins=Sum(Case(When(resultat='win', then=1), output_field=IntegerField(), default=0)),
        losses=Sum(Case(When(resultat='loss', then=1), output_field=IntegerField(), default=0)),
    ).order_by('-mois')[:12]

    ctx = {
        'total': total,
        'wins': wins,
        'losses': losses,
        'voids': voids,
        'taux': taux,
        'stats_sports': stats_sports,
        'historique': historique,
    }
    return render(request, 'pronostics/statistiques.html', ctx)


@login_required
def dashboard(request):
    """Dashboard personnel de l'utilisateur."""
    user = request.user
    notifications = user.notifications.filter(lu=False)[:5]

    ctx = {
        'notifications': notifications,
        'pronostics_recents': Pronostic.objects.filter(publie=True, est_vip=False)[:5],
        'is_vip': user.is_vip,
    }
    return render(request, 'dashboard.html', ctx)
