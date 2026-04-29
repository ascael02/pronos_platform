"""
Modèles pour la gestion des utilisateurs.
Étend le modèle User Django avec des champs personnalisés.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    Ajoute : photo de profil, bio, statut VIP, pays.
    """
    PLAN_FREE = 'free'
    PLAN_VIP = 'vip'
    PLAN_PREMIUM = 'premium'

    PLAN_CHOICES = [
        (PLAN_FREE, 'Gratuit'),
        (PLAN_VIP, 'VIP'),
        (PLAN_PREMIUM, 'Premium'),
    ]

    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True, verbose_name="Photo de profil"
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biographie")
    pays = models.CharField(max_length=100, blank=True, verbose_name="Pays")
    plan = models.CharField(
        max_length=10, choices=PLAN_CHOICES, default=PLAN_FREE, verbose_name="Abonnement"
    )
    vip_expiry = models.DateTimeField(null=True, blank=True, verbose_name="Expiration VIP")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} ({self.email})"

    @property
    def is_vip(self):
        """Vérifie si l'utilisateur a un abonnement VIP actif."""
        if self.plan in (self.PLAN_VIP, self.PLAN_PREMIUM):
            if self.vip_expiry and self.vip_expiry > timezone.now():
                return True
        return False

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.png'

    def activer_vip(self, jours=30):
        """Active le plan VIP pour un nombre de jours donné."""
        if self.vip_expiry and self.vip_expiry > timezone.now():
            self.vip_expiry += timedelta(days=jours)
        else:
            self.vip_expiry = timezone.now() + timedelta(days=jours)
        self.plan = self.PLAN_VIP
        self.save()


class Notification(models.Model):
    """Notifications in-app pour les utilisateurs."""
    TYPE_INFO = 'info'
    TYPE_SUCCESS = 'success'
    TYPE_WARNING = 'warning'

    TYPE_CHOICES = [
        (TYPE_INFO, 'Information'),
        (TYPE_SUCCESS, 'Succès'),
        (TYPE_WARNING, 'Avertissement'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200, verbose_name="Titre")
    message = models.TextField(verbose_name="Message")
    type_notif = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_INFO)
    lu = models.BooleanField(default=False, verbose_name="Lu")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.user.username}] {self.titre}"
