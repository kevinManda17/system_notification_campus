# 🔔 Système de Notifications Campus

Système de notifications d'urgence pour campus universitaire avec dashboards utilisateur et administrateur.

---

## 🎯 Nouveauté: Dashboards Interactifs

### Dashboard Utilisateur
- ✅ Visualisation de toutes vos notifications
- ✅ Statistiques personnelles (total, récentes, haute priorité)
- ✅ Actualisation automatique
- ✅ Design moderne et responsive

### Dashboard Administrateur
- ✅ Vue d'ensemble du système
- ✅ Graphiques interactifs (Chart.js)
- ✅ Top utilisateurs et notifications récentes
- ✅ Statistiques en temps réel

**🚀 Installation rapide:** Double-cliquez sur `install_dashboards.bat` ou consultez [QUICKSTART.md](QUICKSTART.md)

---

## 📁 Structure du projet

systeme_notification/                  # Projet Django
├── manage.py
├── systeme_notification/              # Répertoire du projet
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── notifications/                      # Application principale
    ├── __init__.py
    ├── admin.py                        # Administration Django
    ├── apps.py
    ├── models.py                       # Modèles Django (User, Notification, etc.)
    ├── core.py                         # Classes métiers, mixins, décorateurs, métaclasses
    ├── descriptors.py                  # Descripteurs (Email, Phone, Priority, TimeWindow)
    ├── decorators.py                   # Décorateurs de classes et méthodes
    ├── metaclasses.py                  # Métaclasses (NotificationMeta, ChannelMeta, TemplateMeta, ConfigMeta)
    ├── serializers.py                  # Serializers DRF pour API
    ├── api.py                           # ViewSets / APIViews pour DRF
    ├── views.py                         # Vues pour dashboards
    ├── urls.py                          # Routes API + Dashboards
    ├── templates/                       # Templates HTML
    │   └── notifications/
    │       ├── user_dashboard.html      # Dashboard utilisateur
    │       └── admin_dashboard.html     # Dashboard admin
    └── tests.py                         # Tests unitaires pour tous les concepts

---

## 🌐 URLs Disponibles

| URL | Description | Accès |
|-----|-------------|-------|
| `/dashboard/` | Dashboard utilisateur | Utilisateur connecté |
| `/dashboard/admin/` | Dashboard administrateur | Superuser |
| `/api/notifications/` | API notifications (REST) | Token/Session |
| `/api/stats/` | API statistiques | Token/Session |
| `/api/evacuation/{type}/` | Déclencher évacuation | Token/Session |
| `/admin/` | Interface admin Django | Superuser |

---

## 🚀 Installation

### 1. Cloner le repository
```bash
git clone <repository-url>
cd system_notification_campus
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Installer les dashboards
```bash
# Windows
install_dashboards.bat

# Ou manuellement
python create_dirs.py
```

### 4. Configuration de la base de données
```bash
cd systeme_notification
python manage.py migrate
```

### 5. Créer un superuser
```bash
python manage.py createsuperuser
```

### 6. Créer des données de test (optionnel)
```bash
python create_demo_data.py
```

### 7. Démarrer le serveur
```bash
python manage.py runserver
```

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Guide de démarrage rapide
- **[DASHBOARD_README.md](DASHBOARD_README.md)** - Documentation complète des dashboards
- **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Résumé de l'installation

---

## 🎨 Fonctionnalités

### Système de notifications
- ✅ Notifications personnalisées par utilisateur
- ✅ Priorités (haute, moyenne, faible)
- ✅ Plages horaires configurables
- ✅ Système d'évacuation d'urgence (incendie, inondation, épidémie, sécurité)

### Dashboards
- ✅ Dashboard utilisateur avec notifications personnelles
- ✅ Dashboard admin avec statistiques globales
- ✅ Graphiques interactifs (Chart.js)
- ✅ Actualisation en temps réel

### API REST
- ✅ CRUD complet pour notifications
- ✅ Endpoints d'évacuation d'urgence
- ✅ Statistiques en temps réel

---

## 🛠️ Technologies

- **Backend**: Django 5.2, Django REST Framework
- **Base de données**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **API**: REST API avec DRF
- **Design**: Responsive, moderne, gradients

---

## 🧪 Tests

### Créer des données de démonstration
```bash
cd systeme_notification
python create_demo_data.py
```

Cela créera:
- 4 utilisateurs (alice, bob, charlie, david)
- 13 notifications variées
- Mot de passe: `demo123`

### Accéder aux dashboards
1. **Dashboard Utilisateur**: http://localhost:8000/dashboard/
   - Connectez-vous avec un utilisateur (ex: alice/demo123)

2. **Dashboard Admin**: http://localhost:8000/dashboard/admin/
   - Connectez-vous avec un superuser

---

## 📊 API Examples

### Obtenir les statistiques
```bash
curl http://localhost:8000/api/stats/
```

### Créer une notification
```bash
curl -X POST http://localhost:8000/api/notifications/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Test de notification",
    "destinataire": 1,
    "priority": "haute"
  }'
```

### Déclencher une évacuation
```bash
curl -X POST http://localhost:8000/api/evacuation/incendie/
```

---

## 🎯 Roadmap

- [x] Système de notifications de base
- [x] API REST complète
- [x] Dashboard utilisateur
- [x] Dashboard administrateur
- [x] Graphiques et statistiques
- [ ] Notifications push en temps réel (WebSockets)
- [ ] Application mobile
- [ ] Exportation de rapports (PDF/Excel)
- [ ] Système de filtres avancés
- [ ] Thème sombre (dark mode)

---

## 📝 License

Ce projet est créé pour un usage éducatif.

---

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à ouvrir une issue ou une pull request.

---

**Version**: 1.0  
**Framework**: Django 5.2 + DRF  
**Auteur**: Système de Notifications Campus
