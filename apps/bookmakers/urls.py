from django.urls import path
from . import views

app_name = 'bookmakers'

urlpatterns = [
    path('', views.liste_bookmakers, name='liste'),
    path('<slug:slug>/', views.detail_bookmaker, name='detail'),
    path('<slug:slug>/go/', views.redirect_affilie, name='affilie'),
]
