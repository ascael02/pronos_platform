from django.urls import path
from . import views

app_name = 'vip'

urlpatterns = [
    path('', views.page_vip, name='landing'),
    path('souscrire/<slug:plan_slug>/', views.souscrire, name='souscrire'),
    path('confirmation/<int:pk>/', views.confirmation, name='confirmation'),
]
