from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
import json
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Notification, User
from .core import Epidemie, Incendie, Innondation, Securite



def user_dashboard(request):
    """Dashboard pour les utilisateurs normaux"""
    user = request.user
    notifications = Notification.objects.filter(destinataire=user).order_by('-created_at')
    
    context = {
        'user': user,
        'notifications': notifications,
        'total_notifications': notifications.count(),
        'unread_notifications': notifications.filter(created_at__gte=timezone.now() - timedelta(days=1)).count(),
        'high_priority': notifications.filter(priority='haute').count(),
    }
    return render(request, 'notifications/user_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    """Dashboard pour les administrateurs"""
    # Statistiques générales
    total_users = User.objects.count()
    total_notifications = Notification.objects.count()
    
    # Notifications par priorité
    priority_stats = list(Notification.objects.values('priority').annotate(count=Count('id')))
    
    # Notifications récentes (dernières 24h, 7 jours, 30 jours)
    now = timezone.now()
    notifs_24h = Notification.objects.filter(created_at__gte=now - timedelta(hours=24)).count()
    notifs_7d = Notification.objects.filter(created_at__gte=now - timedelta(days=7)).count()
    notifs_30d = Notification.objects.filter(created_at__gte=now - timedelta(days=30)).count()
    
    # Top 5 utilisateurs avec le plus de notifications
    top_users = User.objects.annotate(
        notif_count=Count('notification')
    ).order_by('-notif_count')[:5]
    
    # Notifications récentes
    recent_notifications = Notification.objects.all().order_by('-created_at')[:10]
    
    # Distribution par jour (derniers 7 jours)
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


@api_view(['GET'])
def stats_api(request):
    """API pour obtenir les statistiques en temps réel"""
    now = timezone.now()
    
    stats = {
        'total_users': User.objects.count(),
        'total_notifications': Notification.objects.count(),
        'notifs_24h': Notification.objects.filter(created_at__gte=now - timedelta(hours=24)).count(),
        'notifs_7d': Notification.objects.filter(created_at__gte=now - timedelta(days=7)).count(),
        'priority_counts': {
            'haute': Notification.objects.filter(priority='haute').count(),
            'moyenne': Notification.objects.filter(priority='moyenne').count(),
            'faible': Notification.objects.filter(priority='faible').count(),
        }
    }
    return Response(stats)


class EvacuationViewSet(viewsets.ViewSet):
    # GET /api/evacuation/epidemie/
    @action(detail=False, methods=["get"])
    def epidemie(self, request):
        return Response({"message": "Évacuation Épidémie prête à être déclenchée"})

    # POST /api/evacuation/epidemie/
    @action(detail=False, methods=["post"])
    def epidemie(self, request):
        e = Epidemie()
        e.evacuer()
        return Response({"status": "Évacuation Épidémie déclenchée"})

    # GET /api/evacuation/incendie/
    @action(detail=False, methods=["get"])
    def incendie(self, request):
        return Response({"message": "Évacuation Incendie prête à être déclenchée"})

    # POST /api/evacuation/incendie/
    @action(detail=False, methods=["post"])
    def incendie(self, request):
        i = Incendie()
        i.evacuer()
        return Response({"status": "Évacuation Incendie déclenchée"})

    # GET /api/evacuation/innondation/
    @action(detail=False, methods=["get"])
    def innondation(self, request):
        return Response({"message": "Évacuation Inondation prête à être déclenchée"})

    # POST /api/evacuation/innondation/
    @action(detail=False, methods=["post"])
    def innondation(self, request):
        n = Innondation()
        n.evacuer()
        return Response({"status": "Évacuation Inondation déclenchée"})

    # GET /api/evacuation/securite/
    @action(detail=False, methods=["get"])
    def securite(self, request):
        return Response({"message": "Évacuation Sécurité prête à être déclenchée"})

    # POST /api/evacuation/securite/
    @action(detail=False, methods=["post"])
    def securite(self, request):
        s = Securite()
        s.evacuer()
        return Response({"status": "Évacuation Sécurité déclenchée"})
