from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

ICONS = {
    'alert': '<path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.9 2.4 17.5A2 2 0 0 0 4.1 20h15.8a2 2 0 0 0 1.7-2.5L13.7 3.9a2 2 0 0 0-3.4 0Z"/>',
    'bank': '<path d="M3 10h18"/><path d="M5 10V20"/><path d="M9 10V20"/><path d="M15 10V20"/><path d="M19 10V20"/><path d="M3 20h18"/><path d="M12 3 4 7h16Z"/>',
    'basketball': '<circle cx="12" cy="12" r="9"/><path d="M4.9 7.5a9 9 0 0 0 14.2 9"/><path d="M4.9 16.5a9 9 0 0 1 14.2-9"/><path d="M12 3a16 16 0 0 0 0 18"/><path d="M12 3a16 16 0 0 1 0 18"/>',
    'bell': '<path d="M10 21h4"/><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/>',
    'calendar': '<path d="M8 2v4"/><path d="M16 2v4"/><path d="M3 10h18"/><rect x="3" y="4" width="18" height="18" rx="2"/>',
    'card': '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/><path d="M6 15h4"/>',
    'chart': '<path d="M3 3v18h18"/><path d="M7 15v-4"/><path d="M12 15V7"/><path d="M17 15v-7"/>',
    'check': '<path d="m20 6-11 11-5-5"/>',
    'chevron-plus': '<path d="M12 5v14"/><path d="M5 12h14"/>',
    'comment': '<path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z"/>',
    'crown': '<path d="m3 7 4 4 5-7 5 7 4-4-2 12H5Z"/><path d="M5 19h14"/>',
    'dashboard': '<path d="M3 13h8V3H3Z"/><path d="M13 21h8V11h-8Z"/><path d="M13 3v6h8V3Z"/><path d="M3 21h8v-6H3Z"/>',
    'diamond': '<path d="M6 3h12l4 6-10 12L2 9Z"/><path d="M2 9h20"/><path d="m8 9 4 12 4-12"/>',
    'edit': '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
    'flame': '<path d="M8.5 14.5A4.5 4.5 0 0 0 13 21a6 6 0 0 0 3.7-10.7c.3 2-1.4 3.2-2.6 3.7.4-3.4-1.4-6.2-4.7-9C9.7 8 7 10.1 7 13a5.5 5.5 0 0 0 1.5 1.5Z"/>',
    'football': '<circle cx="12" cy="12" r="9"/><path d="m12 7 4 3-1.5 5h-5L8 10Z"/><path d="M12 7V3"/><path d="m16 10 4-1"/><path d="m14.5 15 2.5 4"/><path d="m9.5 15-2.5 4"/><path d="M8 10 4 9"/>',
    'home': '<path d="m3 10 9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/>',
    'info': '<path d="M12 16v-4"/><path d="M12 8h.01"/><circle cx="12" cy="12" r="10"/>',
    'key': '<path d="M21 2 11 12"/><circle cx="7.5" cy="15.5" r="5.5"/><path d="m15 8 3 3"/><path d="m18 5 3 3"/>',
    'lock': '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    'newspaper': '<path d="M4 22h14a2 2 0 0 0 2-2V7H8v13a2 2 0 0 1-4 0V5h4"/><path d="M10 12h8"/><path d="M10 16h8"/><path d="M10 8h8"/>',
    'phone': '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/>',
    'spark': '<path d="M12 2v6"/><path d="M12 16v6"/><path d="M2 12h6"/><path d="M16 12h6"/><path d="m4.9 4.9 4.2 4.2"/><path d="m14.9 14.9 4.2 4.2"/><path d="m19.1 4.9-4.2 4.2"/><path d="m9.1 14.9-4.2 4.2"/>',
    'star': '<path d="m12 2 3 6 6.5.9-4.7 4.6 1.1 6.5-5.9-3.1L6.1 20l1.1-6.5L2.5 8.9 9 8Z"/>',
    'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    'rugby': '<path d="M4 20c6.5 0 13-6.5 16-16C10.5 7 4 13.5 4 20Z"/><path d="M7 17 17 7"/><path d="M9 15l-2-2"/><path d="M12 12l-2-2"/><path d="M15 9l-2-2"/>',
    'tennis': '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6c4.6.4 8.4 4.2 8.8 8.8"/><path d="M18.4 18.4c-4.6-.4-8.4-4.2-8.8-8.8"/>',
    'trash': '<path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="m19 6-1 14H6L5 6"/><path d="M10 11v5"/><path d="M14 11v5"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 22a8 8 0 0 1 16 0"/>',
    'view': '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    'x': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
}


@register.simple_tag
def icon(name, classes='w-4 h-4', title=''):
    body = ICONS.get(name, ICONS['info'])
    title_markup = format_html('<title>{}</title>', title) if title else ''
    return mark_safe(
        f'<svg class="{classes}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{title_markup}{body}</svg>'
    )
