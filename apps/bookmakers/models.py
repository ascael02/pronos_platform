"""
Modèles pour la gestion des bookmakers partenaires.
"""

from django.db import models
from django.utils.text import slugify


class Bookmaker(models.Model):
    """
    Bookmaker partenaire avec lien affilié.
    """
    BONUS_TYPE_DEPOT = 'depot'
    BONUS_TYPE_SANS_DEPOT = 'sans_depot'
    BONUS_TYPE_FREEBETS = 'freebets'

    BONUS_CHOICES = [
        (BONUS_TYPE_DEPOT, 'Bonus sur dépôt'),
        (BONUS_TYPE_SANS_DEPOT, 'Bonus sans dépôt'),
        (BONUS_TYPE_FREEBETS, 'Freebets'),
    ]

    nom = models.CharField(max_length=100, unique=True, verbose_name="Bookmaker")
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='bookmakers/', null=True, blank=True, verbose_name="Logo")
    description = models.TextField(blank=True, verbose_name="Description")
    lien_affilie = models.URLField(verbose_name="Lien affilié")
    bonus_montant = models.CharField(max_length=100, blank=True, verbose_name="Montant du bonus")
    bonus_type = models.CharField(
        max_length=20, choices=BONUS_CHOICES,
        default=BONUS_TYPE_DEPOT, verbose_name="Type de bonus"
    )
    note = models.DecimalField(
        max_digits=3, decimal_places=1, default=4.0,
        verbose_name="Note (/5)"
    )
    fiabilite = models.PositiveIntegerField(default=85, verbose_name="Fiabilité (%)")
    disponible_benin = models.BooleanField(default=True, verbose_name="Disponible au Bénin")
    accepte_mobile_money = models.BooleanField(default=True, verbose_name="Mobile Money")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bookmaker"
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class ClicAffilie(models.Model):
    """Suivi des clics sur les liens affiliés (analytics)."""
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE, related_name='clics')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Clic affilié"
        verbose_name_plural = "Clics affiliés"

    def __str__(self):
        return f"Clic → {self.bookmaker.nom} ({self.created_at.strftime('%d/%m/%Y')})"
