# PronosPlatform - Documentation complete

Plateforme de pronostics sportifs Django avec système VIP, API REST, blog SEO et gestion de bookmakers.

---

## Architecture du projet

```
pronos_platform/
├── config/                     # Configuration Django
│   ├── settings.py             # Settings (env-based)
│   ├── urls.py                 # Routes principales
│   └── wsgi.py
│
├── apps/
│   ├── accounts/               # Authentification & utilisateurs
│   │   ├── models.py           # User personnalisé + Notifications
│   │   ├── views.py            # Inscription, connexion, profil
│   │   ├── forms.py
│   │   ├── admin.py            # Admin utilisateurs avec badges VIP
│   │   └── urls.py
│   │
│   ├── pronostics/             # CRUD pronostics (app principale)
│   │   ├── models.py           # Sport, Competition, Match, Pronostic
│   │   ├── views.py            # Liste, détail, CRUD, stats, dashboard
│   │   ├── forms.py
│   │   ├── admin.py            # Admin enrichi avec actions
│   │   ├── context_processors.py
│   │   ├── urls.py
│   │   └── management/
│   │       └── commands/
│   │           └── seed_demo.py  # Données de démo
│   │
│   ├── bookmakers/             # Gestion bookmakers & liens affiliés
│   │   ├── models.py           # Bookmaker + ClicAffilie (analytics)
│   │   ├── views.py
│   │   ├── admin.py
│   │   └── urls.py             # (contient aussi les vues inline)
│   │
│   ├── blog/                   # Blog SEO avec CKEditor
│   │   ├── models.py           # Article + Categorie (SEO, tags)
│   │   ├── views.py
│   │   ├── admin.py
│   │   └── urls.py
│   │
│   ├── vip/                    # Système d'abonnement VIP
│   │   ├── models.py           # PlanAbonnement + Abonnement
│   │   ├── views.py
│   │   ├── context_processors.py
│   │   ├── admin.py
│   │   └── urls.py
│   │
│   └── api/                    # API REST (DRF)
│       ├── views.py            # ViewSets + Serializers
│       └── urls.py             # Router + JWT endpoints
│
├── templates/                  # Templates HTML (Tailwind CSS)
│   ├── base.html               # Layout principal
│   ├── home.html               # Page d'accueil
│   ├── dashboard.html          # Dashboard utilisateur
│   ├── partials/
│   │   └── prono_card.html     # Carte pronostic réutilisable
│   ├── accounts/               # Connexion, inscription, profil
│   ├── pronostics/             # Liste, détail, form, stats
│   ├── bookmakers/             # Liste, détail
│   ├── blog/                   # Liste, détail
│   └── vip/                    # Landing, souscription, confirmation
│
├── static/                     # Fichiers statiques
├── media/                      # Uploads utilisateurs
├── requirements.txt
├── manage.py
└── .env.example
```

---

## Installation complete

### 1. Prérequis

```bash
# Python 3.10+
python --version

# PostgreSQL installé et démarré
psql --version

# Node.js (optionnel, pour Tailwind en prod)
```

### 2. Cloner et préparer l'environnement

```bash
git clone https://github.com/votre-repo/pronos_platform.git
cd pronos_platform

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configurer la base de données PostgreSQL

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Dans psql :
CREATE DATABASE pronos_db;
CREATE USER pronos_user WITH PASSWORD 'pronos_pass';
ALTER ROLE pronos_user SET client_encoding TO 'utf8';
ALTER ROLE pronos_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE pronos_user SET timezone TO 'Africa/Porto-Novo';
GRANT ALL PRIVILEGES ON DATABASE pronos_db TO pronos_user;
\q
```

### 4. Variables d'environnement

```bash
cp .env.example .env
# Éditer .env avec vos valeurs
nano .env
```

### 5. Migrations et données initiales

```bash
# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# OU charger les données de démonstration (recommandé)
python manage.py seed_demo
# → Crée admin@pronos.com / admin1234 + données de démo complètes

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

### 6. Lancer le serveur de développement

```bash
python manage.py runserver
```

**URLs disponibles :**
| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Page d'accueil |
| `http://localhost:8000/admin/` | Interface d'administration |
| `http://localhost:8000/pronostics/` | Liste des pronostics |
| `http://localhost:8000/statistiques/` | Tableau de statistiques |
| `http://localhost:8000/bookmakers/` | Comparatif bookmakers |
| `http://localhost:8000/blog/` | Blog SEO |
| `http://localhost:8000/vip/` | Page VIP |
| `http://localhost:8000/api/v1/` | API REST |
| `http://localhost:8000/api/docs/` | Documentation Swagger |

---

## API REST

### Authentification JWT

```bash
# Obtenir un token
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@pronos.com", "password": "admin1234"}'

# Réponse
{
  "access": "eyJ...",
  "refresh": "eyJ..."
}

# Utiliser le token
curl http://localhost:8000/api/v1/pronostics/ \
  -H "Authorization: Bearer eyJ..."
```

### Endpoints disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/v1/pronostics/` | GET | Liste des pronostics |
| `/api/v1/pronostics/{id}/` | GET | Détail (analyse masquée si VIP) |
| `/api/v1/pronostics/stats/` | GET | Statistiques globales |
| `/api/v1/sports/` | GET | Liste des sports |
| `/api/v1/bookmakers/` | GET | Liste des bookmakers |
| `/api/v1/articles/` | GET | Articles de blog |
| `/api/v1/auth/token/` | POST | Obtenir JWT |
| `/api/v1/auth/token/refresh/` | POST | Rafraîchir JWT |

### Filtres API

```bash
# Filtrer par sport
GET /api/v1/pronostics/?match__competition__sport__slug=football

# Filtrer les gagnants uniquement
GET /api/v1/pronostics/?resultat=win

# Recherche textuelle
GET /api/v1/pronostics/?search=PSG

# Tri
GET /api/v1/pronostics/?ordering=-cote
```

---

## Systeme VIP

Le système VIP fonctionne à trois niveaux :

1. **Modèle** : `User.plan` (free/vip/premium) + `User.vip_expiry`
2. **Pronostic** : `Pronostic.est_vip = True` → analyse masquée
3. **Vue** : Vérification de `user.is_vip` avant d'afficher l'analyse
4. **API** : Même logique dans le `ViewSet.retrieve()`

Pour activer manuellement le VIP d'un utilisateur :
```python
# Dans le shell Django
python manage.py shell
from apps.accounts.models import User
user = User.objects.get(email='user@exemple.com')
user.activer_vip(jours=30)
```

Ou via l'admin Django : `Utilisateurs → Sélectionner → Action "Activer VIP (30 jours)"`

---

## Administration

Interface admin enrichie avec :
- **Badges colorés** pour les statuts (win/loss/pending)
- **Actions groupées** : Marquer comme gagné/perdu, activer VIP
- **Import/Export** CSV pour pronostics et utilisateurs
- **Barres de progression** pour la fiabilité bookmakers
- **Filtres avancés** par sport, résultat, date

**Personnalisation admin dans `config/urls.py` :**
```python
admin.site.site_header = "PronosPlatform Admin"
admin.site.site_title = "PronosPlatform"
admin.site.index_title = "Tableau de bord administrateur"
```

---

## Securite

- `AUTH_USER_MODEL = 'accounts.User'` — modèle User personnalisé
- CSRF activé sur tous les formulaires
- `@login_required` + `@staff_member_required` sur les vues CRUD
- Contrôle VIP côté serveur (pas seulement JS)
- Validation des mots de passe avec les validateurs Django
- Variables sensibles dans `.env` (jamais en dur dans le code)
- En production : HTTPS forcé, HSTS, cookies sécurisés

---

## Deploiement en production

```bash
# Variables .env de production
DEBUG=False
SECRET_KEY=clé-aléatoire-très-longue
ALLOWED_HOSTS=votre-domaine.com

# Gunicorn
gunicorn config.wsgi:application --workers 3 --bind 0.0.0.0:8000

# Nginx (exemple de configuration)
# server {
#     listen 80;
#     server_name votre-domaine.com;
#     location /static/ { alias /path/to/staticfiles/; }
#     location /media/  { alias /path/to/media/; }
#     location / { proxy_pass http://127.0.0.1:8000; }
# }
```

---

## Dependances principales

| Package | Usage |
|---------|-------|
| Django 4.2 | Framework principal |
| djangorestframework | API REST |
| psycopg2-binary | Driver PostgreSQL |
| django-ckeditor-5 | Editeur rich text blog |
| django-taggit | Tags articles blog |
| djangorestframework-simplejwt | Auth JWT API |
| django-import-export | Import/Export CSV admin |
| drf-yasg | Documentation Swagger auto |
| whitenoise | Servir les fichiers statiques |
| python-decouple | Gestion des variables d'env |
| Pillow | Traitement des images |

---

## Developpement

```bash
# Créer de nouvelles migrations après modification des modèles
python manage.py makemigrations
python manage.py migrate

# Shell Django
python manage.py shell

# Tests
python manage.py test

# Vérifier la configuration
python manage.py check --deploy
```

---

*PronosPlatform - Developpe pour le marche de l'Afrique de l'Ouest*
