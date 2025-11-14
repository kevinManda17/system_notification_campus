import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'systeme_notification.settings')
django.setup()

from notifications.models import User, Notification
from django.utils import timezone
from datetime import timedelta

def create_demo_data():
    print("🚀 Création des données de démonstration...\n")
    
    # Supprimer les anciennes données de test
    print("🗑️  Nettoyage des anciennes données...")
    User.objects.filter(username__in=['manda', 'david', 'abi', 'plamse']).delete()
    
    # Créer des utilisateurs
    print("Création des utilisateurs...")
    users = []
    user_data = [
        ('manda','+243997026364', 'manda@campus.com', 'manda b'),
        ('david','+243997026364', 'david@campus.com', 'david b'),
        ('abi','+243997026364', 'abi@campus.com', 'abi b'),
        ('plamse','+243997026364', 'plams@campus.com', 'plamse b'),
    ]
    
    for username, phone, email, full_name in user_data:
        user = User.objects.create_user(
            username=username,
            phone = phone,
            email=email,
            password='demo123',
            first_name=full_name.split()[0],
            last_name=full_name.split()[1]
        )
        users.append(user)
        print(f"   ✅ {username} créé")
    
    # Créer des notifications variées
    print("\n📢 Création des notifications...")
    
    notifications_data = [
        # Notifications pour Alice
        {
            'user': users[0],
            'message': "🔥 ALERTE INCENDIE - Évacuation immédiate du bâtiment A requis. Rendez-vous au point de rassemblement principal.",
            'priority': 'haute',
            'days_ago': 0
        },
        {
            'user': users[0],
            'message': "⚠️ Maintenance électrique programmée demain de 9h à 12h dans les salles 201-210. Prévoir un plan alternatif.",
            'priority': 'moyenne',
            'days_ago': 0
        },
        {
            'user': users[0],
            'message': "📅 Rappel: Exercice d'évacuation trimestriel prévu vendredi prochain à 14h30.",
            'priority': 'faible',
            'days_ago': 1
        },
        {
            'user': users[0],
            'message': "💧 ALERTE INONDATION - Le sous-sol est inondé. Évacuation immédiate des zones concernées.",
            'priority': 'haute',
            'days_ago': 2
        },
        
        # Notifications pour Bob
        {
            'user': users[1],
            'message': "🦠 Nouvelle procédure sanitaire: port du masque obligatoire dans les laboratoires.",
            'priority': 'moyenne',
            'days_ago': 0
        },
        {
            'user': users[1],
            'message': "🔧 Travaux de rénovation: l'accès au parking B sera fermé du 15 au 20 du mois.",
            'priority': 'faible',
            'days_ago': 1
        },
        {
            'user': users[1],
            'message': "⚡ Coupure de courant prévue: sauvegardez vos travaux avant 17h aujourd'hui.",
            'priority': 'haute',
            'days_ago': 3
        },
        
        # Notifications pour Charlie
        {
            'user': users[2],
            'message': "🚨 URGENCE SÉCURITÉ - Intrusion signalée dans le bâtiment C. Restez dans vos locaux.",
            'priority': 'haute',
            'days_ago': 0
        },
        {
            'user': users[2],
            'message': "📋 Mise à jour du plan d'évacuation disponible sur l'intranet.",
            'priority': 'faible',
            'days_ago': 2
        },
        {
            'user': users[2],
            'message': "🌡️ Canicule prévue: mesures de précaution activées. Hydratez-vous régulièrement.",
            'priority': 'moyenne',
            'days_ago': 4
        },
        
        # Notifications pour David
        {
            'user': users[3],
            'message': "🔒 Nouvelle procédure de contrôle d'accès: badge obligatoire à partir de lundi.",
            'priority': 'moyenne',
            'days_ago': 1
        },
        {
            'user': users[3],
            'message': "📞 Numéros d'urgence mis à jour. Consultez l'affichage dans les halls.",
            'priority': 'faible',
            'days_ago': 3
        },
        {
            'user': users[3],
            'message': "🧯 Test des alarmes incendie ce jeudi à 10h. Durée estimée: 15 minutes.",
            'priority': 'moyenne',
            'days_ago': 5
        },
    ]
    
    now = timezone.now()
    for notif_data in notifications_data:
        created_at = now - timedelta(days=notif_data['days_ago'], 
                                      hours=notif_data.get('hours_ago', 0))
        notif = Notification.objects.create(
            destinataire=notif_data['user'],
            message=notif_data['message'],
            priority=notif_data['priority']
        )
        # Modifier manuellement created_at
        notif.created_at = created_at
        notif.save()
        print(f"   ✅ Notification {notif_data['priority']} pour {notif_data['user'].username}")
    
    print(f"\n✨ Succès! {len(notifications_data)} notifications créées pour {len(users)} utilisateurs")
    
    # Afficher les informations de connexion
    print("\n" + "="*60)
    print("📝 INFORMATIONS DE CONNEXION")
    print("="*60)
    print("\n👤 Utilisateurs créés (mot de passe: demo123):")
    for user in users:
        print(f"   • {user.username} - {user.email}")
    
    print("\n🔗 URLs disponibles:")
    print("   • Dashboard utilisateur: http://localhost:8000/dashboard/")
    print("   • Dashboard admin: http://localhost:8000/dashboard/admin/")
    print("   • Admin Django: http://localhost:8000/admin/")
    
    print("\n💡 Pour créer un superuser:")
    print("   python manage.py createsuperuser")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        create_demo_data()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
