"""
Modèles pour le blog SEO de la plateforme.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager
from apps.accounts.models import User


class Categorie(models.Model):
    """Catégorie d'article de blog."""
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    couleur = models.CharField(max_length=7, default='#10B981', verbose_name="Couleur hex")

    class Meta:
        verbose_name = "Catégorie"

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Article(models.Model):
    """Article de blog avec support SEO complet."""
    STATUT_BROUILLON = 'brouillon'
    STATUT_PUBLIE = 'publie'
    STATUT_ARCHIVE = 'archive'

    STATUT_CHOICES = [
        (STATUT_BROUILLON, 'Brouillon'),
        (STATUT_PUBLIE, 'Publié'),
        (STATUT_ARCHIVE, 'Archivé'),
    ]

    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name='articles')
    titre = models.CharField(max_length=300, verbose_name="Titre")
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    extrait = models.TextField(max_length=500, verbose_name="Extrait / Introduction")
    contenu = CKEditor5Field(verbose_name="Contenu", config_name='default')
    image_principale = models.ImageField(
        upload_to='blog/', null=True, blank=True, verbose_name="Image principale"
    )
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default=STATUT_BROUILLON)
    en_vedette = models.BooleanField(default=False, verbose_name="En vedette")
    vues = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)

    # SEO
    meta_titre = models.CharField(max_length=70, blank=True, verbose_name="Meta titre (SEO)")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta description (SEO)")

    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de publication")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Article"
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titre)
            slug = base_slug
            n = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        if self.statut == self.STATUT_PUBLIE and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    @property
    def seo_titre(self):
        return self.meta_titre or self.titre

    @property
    def seo_description(self):
        return self.meta_description or self.extrait[:160]
