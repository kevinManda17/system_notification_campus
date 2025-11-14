# notifications/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Notification, User
from .core import Epidemie, Incendie, Innondation, Securite


# -------------------------------------------------------------------
# USER DASHBOARD (ACCESSIBLE UNIQUEMENT SI CONNECTÉ)
# -------------------------------------------------------------------
@login_required
def user_dashboard(request):
    """Dashboard pour un utilisateur connecté."""
    user = request.user

    notifications = Notification.objects.filter(
        destinataire=user
    ).order_by('-created_at')

    context = {
        'user': user,
        'notifications': notifications,
        'total_notifications': notifications.count(),
        'unread_notifications': notifications.filter(
            created_at__gte=timezone.now() - timedelta(days=1)
        ).count(),
        'high_priority': notifications.filter(priority='HIGH').count(),
    }
    return render(request, 'notifications/user_dashboard.html', context)


# -------------------------------------------------------------------
# ADMIN DASHBOARD (SUPERUSER SEULEMENT)
# -------------------------------------------------------------------
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    """Dashboard administrateur avec statistiques avancées."""
    now = timezone.now()

    # Statistiques globales
    total_users = User.objects.count()
    total_notifications = Notification.objects.count()

    # Par priorité
    priority_stats = list(
        Notification.objects.values('priority').annotate(count=Count('id'))
    )

    # Notifications récentes
    notifs_24h = Notification.objects.filter(created_at__gte=now - timedelta(hours=24)).count()
    notifs_7d  = Notification.objects.filter(created_at__gte=now - timedelta(days=7)).count()
    notifs_30d = Notification.objects.filter(created_at__gte=now - timedelta(days=30)).count()

    # Top utilisateurs
    top_users = User.objects.annotate(
        notif_count=Count('notification')
    ).order_by('-notif_count')[:5]

    # Récents
    recent_notifications = Notification.objects.all().order_by('-created_at')[:10]

    # Stats journalières (sur 7 jours)
    daily_stats = []
    for i in range(7):
        day = now - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        count = Notification.objects.filter(
            created_at__gte=day_start,
            created_at__lt=day_end
        ).count()

        daily_stats.append({
            'date': day_start.strftime('%d/%m'),
            'count': count
        })

    daily_stats.reverse()

    context = {
        'total_users': total_users,
        'total_notifications': total_notifications,
        'priority_stats': priority_stats,
        'notifs_24h': notifs_24h,
        'notifs_7d': notifs_7d,
        'notifs_30d': notifs_30d,
        'top_users': top_users,
        'recent_notifications': recent_notifications,
        'daily_stats': json.dumps(daily_stats),
    }

    return render(request, 'notifications/admin_dashboard.html', context)


# -------------------------------------------------------------------
# STATS API (PUBLIC OU AUTHENTIFIÉ selon usage)
# -------------------------------------------------------------------
@api_view(['GET'])
def stats_api(request):
    """API retournant les statistiques en temps réel."""
    now = timezone.now()

    stats = {
        'total_users': User.objects.count(),
        'total_notifications': Notification.objects.count(),
        'notifs_24h': Notification.objects.filter(created_at__gte=now - timedelta(hours=24)).count(),
        'notifs_7d':  Notification.objects.filter(created_at__gte=now - timedelta(days=7)).count(),
        'priority_counts': {
            'LOW': Notification.objects.filter(priority='LOW').count(),
            'MEDIUM': Notification.objects.filter(priority='MEDIUM').count(),
            'HIGH': Notification.objects.filter(priority='HIGH').count(),
            'URGENT': Notification.objects.filter(priority='URGENT').count(),
        }
    }
    return Response(stats)


# -------------------------------------------------------------------
# VIEWSETS D'ÉVACUATION
# -------------------------------------------------------------------
class EvacuationViewSet(viewsets.ViewSet):

    def _exec(self, obj_class):
        """Exécute l'évacuation et renvoie un message standard."""
        instance = obj_class()
        instance.evacuer()
        return Response({"status": f"Évacuation {obj_class.__name__} déclenchée"})

    # Epidemie (GET + POST)
    def epidemie(self, request):
        if request.method == "POST":
            return self._exec(Epidemie)
        return Response({"message": "Évacuation Epidémie prête"})

    # Incendie
    def incendie(self, request):
        if request.method == "POST":
            return self._exec(Incendie)
        return Response({"message": "Évacuation Incendie prête"})

    # Innondation
    def innondation(self, request):
        if request.method == "POST":
            return self._exec(Innondation)
        return Response({"message": "Évacuation Inondation prête"})

    # Sécurité
    def securite(self, request):
        if request.method == "POST":
            return self._exec(Securite)
        return Response({"message": "Évacuation Sécurité prête"})
