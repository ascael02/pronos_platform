"""
Modèles pour le système VIP et la gestion des abonnements.
"""

from django.db import models
from apps.accounts.models import User


class PlanAbonnement(models.Model):
    """Plan d'abonnement disponible à l'achat."""
    nom = models.CharField(max_length=100, verbose_name="Nom du plan")
    slug = models.SlugField(unique=True)
    prix = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix (FCFA)")
    duree_jours = models.PositiveIntegerField(verbose_name="Durée (jours)")
    description = models.TextField(blank=True)
    fonctionnalites = models.JSONField(default=list, verbose_name="Liste des fonctionnalités")
    populaire = models.BooleanField(default=False, verbose_name="Plan populaire")
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Plan d'abonnement"
        ordering = ['prix']

    def __str__(self):
        return f"{self.nom} – {self.prix} FCFA / {self.duree_jours}j"


class Abonnement(models.Model):
    """Historique des abonnements utilisateurs."""
    STATUT_ACTIF = 'actif'
    STATUT_EXPIRE = 'expire'
    STATUT_ANNULE = 'annule'

    STATUT_CHOICES = [
        (STATUT_ACTIF, 'Actif'),
        (STATUT_EXPIRE, 'Expiré'),
        (STATUT_ANNULE, 'Annulé'),
    ]

    PAIEMENT_MOMO = 'momo'
    PAIEMENT_CARD = 'card'
    PAIEMENT_CRYPTO = 'crypto'

    PAIEMENT_CHOICES = [
        (PAIEMENT_MOMO, 'Mobile Money'),
        (PAIEMENT_CARD, 'Carte bancaire'),
        (PAIEMENT_CRYPTO, 'Crypto'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='abonnements')
    plan = models.ForeignKey(PlanAbonnement, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default=STATUT_ACTIF)
    methode_paiement = models.CharField(max_length=10, choices=PAIEMENT_CHOICES, default=PAIEMENT_MOMO)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)
    reference_paiement = models.CharField(max_length=200, blank=True, verbose_name="Référence paiement")
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField()

    class Meta:
        verbose_name = "Abonnement"
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.user.username} – {self.plan} ({self.statut})"
