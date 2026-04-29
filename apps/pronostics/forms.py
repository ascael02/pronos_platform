"""
Formulaires pour les pronostics.
"""

from django import forms
from .models import Pronostic, Match, CommentairePronostic


class PronosticForm(forms.ModelForm):
    class Meta:
        model = Pronostic
        fields = [
            'match', 'titre', 'prediction', 'cote',
            'mise_recommandee', 'analyse', 'confiance',
            'est_vip', 'publie', 'bookmaker',
        ]
        widgets = {
            'analyse': forms.Textarea(attrs={'rows': 6, 'class': 'w-full rounded-lg border border-gray-600 bg-gray-800 text-white p-3'}),
            'titre': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-600 bg-gray-800 text-white p-3'}),
            'prediction': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-600 bg-gray-800 text-white p-3', 'placeholder': 'Ex: 1, X, 2, BTTS, +2.5'}),
            'cote': forms.NumberInput(attrs={'class': 'w-full rounded-lg border border-gray-600 bg-gray-800 text-white p-3', 'step': '0.01'}),
            'mise_recommandee': forms.NumberInput(attrs={'class': 'w-full rounded-lg border border-gray-600 bg-gray-800 text-white p-3', 'step': '0.5'}),
        }


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['competition', 'equipe_domicile', 'equipe_exterieur', 'date_match']
        widgets = {
            'date_match': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full rounded-lg border border-gray-600 bg-gray-800 text-white p-3'}),
        }


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = CommentairePronostic
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Partagez votre avis...',
                'class': 'w-full rounded-lg border border-gray-600 bg-gray-800 text-white p-3 resize-none',
            })
        }
        labels = {'contenu': ''}
