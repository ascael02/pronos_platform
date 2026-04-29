from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PlanAbonnement, Abonnement
from apps.pronostics.models import Pronostic


def page_vip(request):
    plans = PlanAbonnement.objects.filter(actif=True)
    pronos_vip = Pronostic.objects.filter(publie=True, est_vip=True)[:6]
    return render(request, 'vip/landing.html', {'plans': plans, 'pronos_vip': pronos_vip})


@login_required
def souscrire(request, plan_slug):
    plan = get_object_or_404(PlanAbonnement, slug=plan_slug, actif=True)
    if request.method == 'POST':
        from django.utils import timezone
        from datetime import timedelta
        abonnement = Abonnement.objects.create(
            user=request.user, plan=plan, montant_paye=plan.prix,
            methode_paiement=request.POST.get('methode_paiement', 'momo'),
            reference_paiement=request.POST.get('reference', ''),
            date_fin=timezone.now() + timedelta(days=plan.duree_jours),
        )
        request.user.activer_vip(jours=plan.duree_jours)
        messages.success(request, f"Abonnement {plan.nom} active !")
        return redirect('vip:confirmation', pk=abonnement.pk)
    return render(request, 'vip/souscrire.html', {'plan': plan})


@login_required
def confirmation(request, pk):
    abonnement = get_object_or_404(Abonnement, pk=pk, user=request.user)
    return render(request, 'vip/confirmation.html', {'abonnement': abonnement})
