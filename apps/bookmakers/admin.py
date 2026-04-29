from django.contrib import admin
from django.utils.html import format_html
from .models import Bookmaker, ClicAffilie


@admin.register(Bookmaker)
class BookmakerAdmin(admin.ModelAdmin):
    list_display = [
        'logo_preview',
        'nom',
        'bonus_montant',
        'note_score',
        'fiabilite_bar',
        'disponible_benin',
        'actif',
        'ordre',
        'total_clics',
    ]
    list_filter = ['actif', 'disponible_benin', 'accepte_mobile_money']
    list_editable = ['actif', 'ordre']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',)}
    ordering = ['ordre']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:32px;border-radius:4px">',
                obj.logo.url,
            )
        return '-'
    logo_preview.short_description = 'Logo'

    def note_score(self, obj):
        return format_html(
            '<span style="color:#f59e0b;font-weight:700">{}</span><span style="color:#9ca3af">/5</span>',
            obj.note,
        )
    note_score.short_description = 'Note'

    def fiabilite_bar(self, obj):
        color = (
            '#10b981' if obj.fiabilite >= 80 else
            '#f59e0b' if obj.fiabilite >= 60 else
            '#ef4444'
        )
        return format_html(
            '<div style="width:100px;background:#1f2937;border-radius:4px;overflow:hidden">'
            '<div style="width:{}%;background:{};height:10px;border-radius:4px"></div>'
            '</div> {}%',
            obj.fiabilite,
            color,
            obj.fiabilite,
        )
    fiabilite_bar.short_description = 'Fiabilité'

    def total_clics(self, obj):
        return obj.clics.count()
    total_clics.short_description = 'Clics affiliés'


@admin.register(ClicAffilie)
class ClicAffilieAdmin(admin.ModelAdmin):
    list_display = ['bookmaker', 'ip_address', 'created_at']
    list_filter = ['bookmaker']
    date_hierarchy = 'created_at'
    readonly_fields = ['bookmaker', 'ip_address', 'user_agent', 'created_at']
