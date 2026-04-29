"""
Context processor pour le statut VIP utilisateur.
"""


def vip_status(request):
    """Injecte le statut VIP dans tous les templates."""
    if request.user.is_authenticated:
        return {
            'user_is_vip': request.user.is_vip,
            'user_plan': request.user.plan,
            'vip_expiry': request.user.vip_expiry,
        }
    return {'user_is_vip': False, 'user_plan': 'free'}
