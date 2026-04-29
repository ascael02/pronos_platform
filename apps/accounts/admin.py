from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import User, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    list_display = ['username', 'email', 'plan_badge', 'pays', 'is_vip', 'date_joined']
    list_filter = ['plan', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'pays']
    ordering = ['-date_joined']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profil', {'fields': ('avatar', 'bio', 'pays', 'telephone')}),
        ('Abonnement VIP', {'fields': ('plan', 'vip_expiry')}),
    )

    def plan_badge(self, obj):
        colors = {'free': '#6b7280', 'vip': '#f59e0b', 'premium': '#8b5cf6'}
        color = colors.get(obj.plan, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:9999px;font-size:11px">{}</span>',
            color,
            obj.get_plan_display(),
        )
    plan_badge.short_description = 'Plan'

    @admin.action(description='Activer VIP (30 jours)')
    def activer_vip_30(self, request, queryset):
        for user in queryset:
            user.activer_vip(jours=30)
        self.message_user(request, f'{queryset.count()} utilisateur(s) passés VIP.')

    actions = ['activer_vip_30']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'titre', 'type_notif', 'lu', 'created_at']
    list_filter = ['type_notif', 'lu']
    search_fields = ['user__username', 'titre']
