from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import Sport, Competition, Match, Pronostic, CommentairePronostic


class CommentaireInline(admin.TabularInline):
    model = CommentairePronostic
    extra = 0
    readonly_fields = ['auteur', 'created_at']


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ['icone', 'nom', 'slug', 'actif']
    prepopulated_fields = {'slug': ('nom',)}
    list_editable = ['actif']


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['nom', 'sport', 'pays', 'actif']
    list_filter = ['sport', 'actif']
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ['nom', 'pays']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'competition', 'date_match', 'score_display', 'termine']
    list_filter = ['competition__sport', 'termine']
    search_fields = ['equipe_domicile', 'equipe_exterieur']
    date_hierarchy = 'date_match'


@admin.register(Pronostic)
class PronosticAdmin(ImportExportModelAdmin):
    list_display = [
        'titre_court',
        'match',
        'prediction',
        'cote',
        'resultat',
        'resultat_badge',
        'confiance_score',
        'est_vip',
        'vues',
        'created_at',
    ]
    list_filter = ['resultat', 'est_vip', 'publie', 'match__competition__sport']
    search_fields = ['titre', 'match__equipe_domicile', 'match__equipe_exterieur']
    date_hierarchy = 'created_at'
    readonly_fields = ['vues', 'slug']
    inlines = [CommentaireInline]
    list_editable = ['resultat']
    list_per_page = 25

    def titre_court(self, obj):
        return obj.titre[:50] + '...' if len(obj.titre) > 50 else obj.titre
    titre_court.short_description = 'Titre'

    def resultat_badge(self, obj):
        colors = {
            'pending': ('#6b7280', 'Attente'),
            'win': ('#10b981', 'Gagné'),
            'loss': ('#ef4444', 'Perdu'),
            'void': ('#f59e0b', 'Remb.'),
        }
        color, label = colors.get(obj.resultat, ('#6b7280', obj.resultat))
        return format_html(
            '<span style="background:{};color:white;padding:2px 10px;border-radius:9999px">{}</span>',
            color,
            label,
        )
    resultat_badge.short_description = 'Résultat'

    def confiance_score(self, obj):
        return format_html(
            '<span style="color:#f59e0b;font-weight:700">{}</span><span style="color:#9ca3af">/5</span>',
            int(obj.confiance or 0),
        )
    confiance_score.short_description = 'Confiance'

    @admin.action(description='Marquer GAGNÉ')
    def marquer_win(self, request, queryset):
        queryset.update(resultat='win')

    @admin.action(description='Marquer PERDU')
    def marquer_loss(self, request, queryset):
        queryset.update(resultat='loss')

    actions = ['marquer_win', 'marquer_loss']


@admin.register(CommentairePronostic)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ['auteur', 'pronostic', 'approuve', 'created_at']
    list_editable = ['approuve']
    list_filter = ['approuve']
