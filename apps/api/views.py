from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.pronostics.models import Pronostic, Sport
from apps.bookmakers.models import Bookmaker
from apps.blog.models import Article
from .serializers import (
    PronosticListSerializer, PronosticDetailSerializer,
    SportSerializer, BookmakerSerializer, ArticleSerializer
)


class PronosticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pronostic.objects.filter(publie=True).select_related(
        'match', 'match__competition', 'auteur', 'bookmaker'
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['resultat', 'est_vip']
    search_fields = ['titre', 'match__equipe_domicile', 'match__equipe_exterieur']
    ordering_fields = ['created_at', 'cote', 'confiance']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PronosticDetailSerializer
        return PronosticListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if instance.est_vip:
            if not request.user.is_authenticated or not getattr(request.user, 'is_vip', False):
                data['analyse'] = "Contenu VIP. Abonnez-vous pour acceder a l'analyse complete."
        return Response(data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        from django.db.models import Count
        qs = self.queryset.exclude(resultat='pending')
        total = qs.count()
        wins = qs.filter(resultat='win').count()
        return Response({
            'total': total,
            'wins': wins,
            'losses': qs.filter(resultat='loss').count(),
            'taux_reussite': round(wins / total * 100, 1) if total else 0,
        })


class SportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sport.objects.filter(actif=True)
    serializer_class = SportSerializer


class BookmakerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bookmaker.objects.filter(actif=True)
    serializer_class = BookmakerSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.filter(statut='publie').select_related('auteur', 'categorie')
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titre', 'extrait']
