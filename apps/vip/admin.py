from django.contrib import admin
from .models import PlanAbonnement, Abonnement


@admin.register(PlanAbonnement)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prix', 'duree_jours', 'populaire', 'actif']
    list_editable = ['populaire', 'actif']
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'statut', 'methode_paiement', 'montant_paye', 'date_fin']
    list_filter = ['statut', 'methode_paiement', 'plan']
    search_fields = ['user__username', 'user__email', 'reference_paiement']
    date_hierarchy = 'date_debut'
    readonly_fields = ['date_debut']
