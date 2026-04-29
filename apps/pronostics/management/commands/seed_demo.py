"""
Commande Django pour charger des données de démonstration.
Usage : python manage.py seed_demo
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = "Charge des données de démonstration pour PronosPlatform"

    def handle(self, *args, **options):
        self.stdout.write("[seed] Chargement des donnees de demonstration...")

        # ─── Sports ───────────────────────────────────────────────────────────
        from apps.pronostics.models import Sport, Competition, Match, Pronostic

        sports_data = [
            ('Football', 'football', 'football'),
            ('Basketball', 'basketball', 'basketball'),
            ('Tennis', 'tennis', 'tennis'),
            ('Rugby', 'rugby', 'rugby'),
        ]
        sports = {}
        for nom, slug, icone in sports_data:
            sport, _ = Sport.objects.get_or_create(slug=slug, defaults={'nom': nom, 'icone': icone})
            sports[slug] = sport
            self.stdout.write(f"  [ok] Sport: {nom}")

        # ─── Compétitions ─────────────────────────────────────────────────────
        comps_data = [
            ('Ligue 1', 'ligue-1', 'France', 'football'),
            ('Champions League', 'champions-league', 'Europe', 'football'),
            ('Premier League', 'premier-league', 'Angleterre', 'football'),
            ('Ligue UEMOA', 'ligue-uemoa', 'Afrique de l\'Ouest', 'football'),
            ('NBA', 'nba', 'USA', 'basketball'),
        ]
        comps = {}
        for nom, slug, pays, sport_slug in comps_data:
            comp, _ = Competition.objects.get_or_create(
                slug=slug,
                defaults={'nom': nom, 'pays': pays, 'sport': sports[sport_slug]}
            )
            comps[slug] = comp
            self.stdout.write(f"  [ok] Competition: {nom}")

        # ─── Bookmakers ───────────────────────────────────────────────────────
        from apps.bookmakers.models import Bookmaker
        bk_data = [
            ('1xBet', '1xbet', 'https://1xbet.com/?ref=demo', '200% jusqu\'à 200 000 FCFA', 4.3, 88),
            ('Betway', 'betway', 'https://betway.com/?ref=demo', '100% jusqu\'à 100 000 FCFA', 4.5, 92),
            ('Melbet', 'melbet', 'https://melbet.com/?ref=demo', '130% jusqu\'à 130 000 FCFA', 4.0, 82),
            ('22Bet', '22bet', 'https://22bet.com/?ref=demo', '122% jusqu\'à 122 000 FCFA', 3.8, 78),
        ]
        bookmakers = {}
        for nom, slug, url, bonus, note, fiabilite in bk_data:
            bk, _ = Bookmaker.objects.get_or_create(
                slug=slug,
                defaults={
                    'nom': nom, 'lien_affilie': url, 'bonus_montant': bonus,
                    'note': note, 'fiabilite': fiabilite, 'disponible_benin': True,
                    'accepte_mobile_money': True
                }
            )
            bookmakers[slug] = bk
            self.stdout.write(f"  [ok] Bookmaker: {nom}")

        # ─── Plans VIP ────────────────────────────────────────────────────────
        from apps.vip.models import PlanAbonnement
        plans_data = [
            ('Starter', 'starter', 2000, 7, ['Accès aux pronostics VIP', 'Analyse complète', 'Support email'], False),
            ('Pro', 'pro', 5000, 30, ['Accès aux pronostics VIP', 'Analyse complète', 'Alertes instantanées', 'Stats avancées', 'Support prioritaire'], True),
            ('Elite', 'elite', 15000, 90, ['Accès illimité VIP', 'Toutes les fonctionnalités Pro', 'Accès Discord privé', 'Coaching personnalisé'], False),
        ]
        for nom, slug, prix, duree, features, populaire in plans_data:
            PlanAbonnement.objects.get_or_create(
                slug=slug,
                defaults={
                    'nom': nom, 'prix': prix, 'duree_jours': duree,
                    'fonctionnalites': features, 'populaire': populaire
                }
            )
            self.stdout.write(f"  [ok] Plan VIP: {nom}")

        # ─── Matchs ───────────────────────────────────────────────────────────
        matchs_data = [
            ('PSG', 'Real Madrid', 'champions-league', 1),
            ('Manchester City', 'Arsenal', 'premier-league', 2),
            ('AS Monaco', 'OGC Nice', 'ligue-1', -1),
            ('Barcelona', 'Atletico Madrid', 'champions-league', 3),
            ('Séwé SC', 'ASPAC', 'ligue-uemoa', -2),
            ('LA Lakers', 'Golden State Warriors', 'nba', 0),
        ]
        matchs = []
        for dom, ext, comp_slug, delta in matchs_data:
            m, _ = Match.objects.get_or_create(
                equipe_domicile=dom,
                equipe_exterieur=ext,
                competition=comps[comp_slug],
                defaults={'date_match': timezone.now() + timedelta(days=delta)}
            )
            matchs.append(m)
        self.stdout.write(f"  [ok] {len(matchs)} matchs crees")

        # ─── Pronostics ───────────────────────────────────────────────────────
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin = User.objects.filter(is_staff=True).first()
        if not admin:
            admin = User.objects.create_superuser('admin', 'admin@pronos.com', 'admin1234')
            self.stdout.write("  [ok] Superuser cree: admin / admin1234")

        pronos_data = [
            ('PSG gagne avec au moins 2 buts d\'écart', matchs[0], '1 & +1.5', 1.85, False, 4, 'win',
             "Le PSG traverse une forme exceptionnelle avec 7 victoires consécutives. Face au Real Madrid sans Bellingham, l'avantage à domicile est déterminant."),
            ('Les deux équipes marquent à Etihad', matchs[1], 'BTTS', 1.65, False, 3, 'win',
             "Manchester City et Arsenal se distinguent par leurs attaques prolifiques. Ces deux équipes ont marqué dans 80% de leurs confrontations récentes."),
            ('Monaco s\'impose à domicile', matchs[2], '1', 1.95, False, 4, 'pending',
             "Monaco évolue à un excellent niveau cette saison. Sur leur pelouse du Rocher, ils restent sur 6 victoires en 7 matches."),
            ('Séwé SC domine le derby', matchs[4], '1', 1.75, True, 5, 'pending',
             "Analyse VIP exclusive : Le Séwé Sport Club bénéficie d'un effectif complet et d'une série de 8 matches sans défaite à domicile cette saison. Les données statistiques montrent une domination territoriale de 64% en moyenne. Notre analyse approfondie prédit une victoire convaincante."),
            ('Over 2.5 buts PSG vs Real', matchs[0], '+2.5', 1.75, False, 3, 'win',
             "Ces deux mastodontes européens ont systématiquement produit des rencontres avec beaucoup de buts. La moyenne de buts dans leurs confrontations directes dépasse 3.2."),
        ]

        for titre, match, pred, cote, vip, conf, resultat, analyse in pronos_data:
            Pronostic.objects.get_or_create(
                titre=titre,
                defaults={
                    'match': match, 'prediction': pred, 'cote': cote,
                    'est_vip': vip, 'confiance': conf, 'resultat': resultat,
                    'analyse': analyse, 'auteur': admin,
                    'bookmaker': bookmakers.get('1xbet')
                }
            )
        self.stdout.write("  [ok] Pronostics crees")

        # ─── Blog ─────────────────────────────────────────────────────────────
        from apps.blog.models import Categorie, Article
        cat, _ = Categorie.objects.get_or_create(
            slug='guides',
            defaults={'nom': 'Guides', 'couleur': '#10B981'}
        )
        Article.objects.get_or_create(
            slug='comment-gagner-avec-les-paris-sportifs',
            defaults={
                'titre': 'Comment gagner régulièrement avec les paris sportifs en 2024',
                'extrait': 'Découvrez les stratégies des parieurs professionnels pour maximiser vos gains sur le long terme.',
                'contenu': '<h2>Les fondamentaux du parieur professionnel</h2><p>Les parieurs qui gagnent sur le long terme ne misent pas au hasard. Ils appliquent des stratégies éprouvées basées sur des données statistiques solides...</p><h2>La gestion du bankroll</h2><p>La règle d\'or : ne jamais miser plus de 2-5% de votre capital sur un seul événement. Cette approche vous protège des mauvaises séries...</p>',
                'auteur': admin,
                'categorie': cat,
                'statut': 'publie',
                'published_at': timezone.now(),
                'meta_titre': 'Comment gagner avec les paris sportifs — Guide 2024',
                'meta_description': 'Stratégies et conseils des experts pour rentabiliser vos paris sportifs.',
            }
        )
        self.stdout.write("  [ok] Article de blog cree")

        self.stdout.write(self.style.SUCCESS('\nDonnees de demonstration chargees avec succes !'))
        self.stdout.write(self.style.SUCCESS('   Admin : admin@pronos.com / admin1234'))
        self.stdout.write(self.style.SUCCESS('   URL admin : http://localhost:8000/admin/'))
