from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from apps.pronostics.models import Pronostic, Match, Sport, Competition
from apps.bookmakers.models import Bookmaker
from apps.blog.models import Article


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['id', 'nom', 'slug', 'icone']


class CompetitionSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)

    class Meta:
        model = Competition
        fields = ['id', 'nom', 'slug', 'pays', 'sport']


class MatchSerializer(serializers.ModelSerializer):
    competition = CompetitionSerializer(read_only=True)
    score_display = serializers.SerializerMethodField()

    @extend_schema_field(str)
    def get_score_display(self, obj):
        return obj.score_display

    class Meta:
        model = Match
        fields = ['id', 'competition', 'equipe_domicile', 'equipe_exterieur',
                  'date_match', 'score_display', 'termine']


class PronosticListSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    auteur = serializers.StringRelatedField()
    resultat_display = serializers.CharField(source='get_resultat_display', read_only=True)

    class Meta:
        model = Pronostic
        fields = ['id', 'titre', 'slug', 'match', 'prediction', 'cote',
                  'confiance', 'resultat', 'resultat_display', 'est_vip',
                  'auteur', 'vues', 'created_at']


class PronosticDetailSerializer(PronosticListSerializer):
    class Meta(PronosticListSerializer.Meta):
        fields = PronosticListSerializer.Meta.fields + ['analyse', 'mise_recommandee']


class BookmakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmaker
        fields = ['id', 'nom', 'slug', 'bonus_montant', 'note',
                  'fiabilite', 'disponible_benin', 'accepte_mobile_money']


class ArticleSerializer(serializers.ModelSerializer):
    auteur = serializers.StringRelatedField()
    categorie = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = ['id', 'titre', 'slug', 'extrait', 'categorie', 'auteur', 'vues', 'published_at']
