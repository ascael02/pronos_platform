from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Categorie


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'couleur_preview', 'slug']
    prepopulated_fields = {'slug': ('nom',)}

    def couleur_preview(self, obj):
        return format_html(
            '<span style="background:{};padding:4px 12px;border-radius:4px;color:white">{}</span>',
            obj.couleur,
            obj.couleur,
        )
    couleur_preview.short_description = 'Couleur'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'titre_court',
        'auteur',
        'categorie',
        'statut',
        'statut_badge',
        'en_vedette',
        'vues',
        'published_at',
    ]
    list_filter = ['statut', 'en_vedette', 'categorie']
    search_fields = ['titre', 'extrait']
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'published_at'
    list_editable = ['statut', 'en_vedette']
    readonly_fields = ['vues']
    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'slug', 'extrait', 'contenu', 'image_principale')
        }),
        ('Classification', {
            'fields': ('auteur', 'categorie', 'tags')
        }),
        ('Publication', {
            'fields': ('statut', 'en_vedette', 'published_at', 'vues')
        }),
        ('SEO', {
            'fields': ('meta_titre', 'meta_description'),
            'classes': ('collapse',),
        }),
    )

    def titre_court(self, obj):
        return obj.titre[:60] + '...' if len(obj.titre) > 60 else obj.titre
    titre_court.short_description = 'Titre'

    def statut_badge(self, obj):
        colors = {
            'brouillon': '#6b7280',
            'publie': '#10b981',
            'archive': '#ef4444',
        }
        labels = {
            'brouillon': 'Brouillon',
            'publie': 'Publié',
            'archive': 'Archivé',
        }
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:9999px;font-size:11px">{}</span>',
            colors.get(obj.statut, '#6b7280'),
            labels.get(obj.statut, obj.statut),
        )
    statut_badge.short_description = 'Statut'
