# apps/pronostics/urls.py
from django.urls import path
from . import views

app_name = 'pronostics'

urlpatterns = [
    path('', views.home, name='home'),
    path('pronostics/', views.liste_pronostics, name='liste'),
    # ─── Routes statiques AVANT les patterns dynamiques ──────────────────────
    path('pronostics/nouveau/', views.creer_pronostic, name='creer'),
    path('statistiques/', views.statistiques, name='stats'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # ─── Routes dynamiques avec slug ─────────────────────────────────────────
    path('pronostics/<slug:slug>/modifier/', views.modifier_pronostic, name='modifier'),
    path('pronostics/<slug:slug>/supprimer/', views.supprimer_pronostic, name='supprimer'),
    path('pronostics/<slug:slug>/', views.detail_pronostic, name='detail'),
]
