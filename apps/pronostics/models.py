"""
Modèles pour la gestion des pronostics sportifs.
Couvre : Sports, Compétitions, Matchs, Pronostics, Résultats.
"""

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from apps.accounts.models import User


class Sport(models.Model):
    """Catégorie sportive (Football, Basketball, Tennis...)."""
    nom = models.CharField(max_length=100, unique=True, verbose_name="Sport")
    slug = models.SlugField(unique=True)
    icone = models.CharField(max_length=50, default='football', verbose_name="Icone SVG")
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sport"
        ordering = ['nom']

    def __str__(self):
        return f"{self.icone} {self.nom}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Competition(models.Model):
    """Compétition / Ligue (Ligue 1, Champions League...)."""
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='competitions')
    nom = models.CharField(max_length=200, verbose_name="Compétition")
    slug = models.SlugField(unique=True)
    pays = models.CharField(max_length=100, blank=True, verbose_name="Pays")
    logo = models.ImageField(upload_to='competitions/', null=True, blank=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Compétition"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Match(models.Model):
    """Match sportif."""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='matchs')
    equipe_domicile = models.CharField(max_length=200, verbose_name="Équipe domicile")
    equipe_exterieur = models.CharField(max_length=200, verbose_name="Équipe extérieur")
    date_match = models.DateTimeField(verbose_name="Date et heure")
    score_domicile = models.PositiveIntegerField(null=True, blank=True)
    score_exterieur = models.PositiveIntegerField(null=True, blank=True)
    termine = models.BooleanField(default=False, verbose_name="Terminé")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matchs"
        ordering = ['-date_match']

    def __str__(self):
        return f"{self.equipe_domicile} vs {self.equipe_exterieur}"

    @property
    def score_display(self):
        if self.score_domicile is not None and self.score_exterieur is not None:
            return f"{self.score_domicile} - {self.score_exterieur}"
        return "- : -"


class Pronostic(models.Model):
    """
    Pronostic sur un match.
    Peut être public (gratuit) ou VIP (accès restreint).
    """
    RESULTAT_PENDING = 'pending'
    RESULTAT_WIN = 'win'
    RESULTAT_LOSS = 'loss'
    RESULTAT_VOID = 'void'  # Match annulé / remboursé

    RESULTAT_CHOICES = [
        (RESULTAT_PENDING, '⏳ En attente'),
        (RESULTAT_WIN, 'Gagné'),
        (RESULTAT_LOSS, 'Perdu'),
        (RESULTAT_VOID, 'Remboursé'),
    ]

    CONFIANCE_CHOICES = [(i, f"{i}/5 ⭐") for i in range(1, 6)]

    auteur = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='pronostics'
    )
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='pronostics')
    titre = models.CharField(max_length=300, verbose_name="Titre du pronostic")
    slug = models.SlugField(unique=True, blank=True)
    prediction = models.CharField(max_length=200, verbose_name="Prédiction (ex: 1, X, 2, BTTS)")
    cote = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cote")
    mise_recommandee = models.DecimalField(
        max_digits=5, decimal_places=2, default=5.00,
        verbose_name="Mise recommandée (%)"
    )
    analyse = models.TextField(verbose_name="Analyse détaillée")
    confiance = models.IntegerField(choices=CONFIANCE_CHOICES, default=3, verbose_name="Confiance")
    resultat = models.CharField(
        max_length=10, choices=RESULTAT_CHOICES, default=RESULTAT_PENDING
    )
    est_vip = models.BooleanField(default=False, verbose_name="Réservé VIP")
    publie = models.BooleanField(default=True, verbose_name="Publié")
    bookmaker = models.ForeignKey(
        'bookmakers.Bookmaker', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='pronostics'
    )
    vues = models.PositiveIntegerField(default=0, verbose_name="Vues")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pronostic"
        ordering = ['-created_at']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titre)
            slug = base_slug
            n = 1
            while Pronostic.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pronostics:detail', kwargs={'slug': self.slug})

    @property
    def est_gagne(self):
        return self.resultat == self.RESULTAT_WIN

    @property
    def retour_potentiel(self):
        """Calcule le retour potentiel pour 100 unités misées."""
        return round(float(self.cote) * 100, 2)


class CommentairePronostic(models.Model):
    """Commentaires des utilisateurs sur les pronostics."""
    pronostic = models.ForeignKey(Pronostic, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField(max_length=1000, verbose_name="Commentaire")
    approuve = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.auteur.username} → {self.pronostic.titre[:40]}"
