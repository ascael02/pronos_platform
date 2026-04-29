"""
Injecte les statistiques globales dans tous les templates.
"""

from django.core.cache import cache


def global_stats(request):
    """Calcule et met en cache les stats globales (TTL 10 min)."""
    stats = cache.get('global_pronos_stats')

    if stats is None:
        try:
            from apps.pronostics.models import Pronostic
            qs = Pronostic.objects.filter(publie=True).exclude(resultat='pending')
            total = qs.count()
            wins = qs.filter(resultat='win').count()
            stats = {
                'global_total': total,
                'global_wins': wins,
                'global_taux': round(wins / total * 100, 1) if total else 0,
            }
            cache.set('global_pronos_stats', stats, 600)
        except Exception:
            stats = {'global_total': 0, 'global_wins': 0, 'global_taux': 0}

    return stats
